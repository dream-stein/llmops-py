#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/6 15:38
#Author  :Emcikem
@File    :api_tool_service.py
"""
import json
from typing import Any
from uuid import UUID

from injector import inject
from dataclasses import dataclass

from sqlalchemy import desc

from internal.exception import ValidateErrorException, NotFoundException
from internal.core.tools.api_tools.entities import OpenAPISchema
from internal.schema.api_tool_schema import (
    CreateApiToolReq,
    GetApiToolProvidersWithPageReq,
    UpdateApiToolProviderReq,
)
from pkg.paginator import Paginator
from pkg.sqlalchemy import SQLAlchemy
from .base_service import BaseService
from internal.model import ApiToolProvider, ApiTool, Account
from internal.core.tools.api_tools.providers import ApiProviderManager

@inject
@dataclass
class ApiToolService(BaseService):
    """自定义API插件服务"""
    db: SQLAlchemy
    api_provider_manager: ApiProviderManager

    def update_api_tool_provider(
            self,
            provider_id: UUID,
            req: UpdateApiToolProviderReq,
            account: Account,
    ):
        """根据传递的provider_id+req更新的API工具提供者信息"""
        # 1.根据传递的provider_id查找APPi工具提供者信息并校验
        api_tool_provider = self.get(ApiToolProvider, provider_id)
        if api_tool_provider is None or api_tool_provider.account_id != account.id:
            raise ValidateErrorException("该工具提供者不存在")

        # 2.校验openapi_schema数据
        openapi_schema = self.parse_openapi_schema(req.openapi_schema.data)

        # 3.检测当前账号是否已经创建了同名的工具提供者，如果是则抛出错误
        check_api_tool_provider = self.db.session.query(ApiToolProvider).filter(
            ApiToolProvider.account_id == account.id,
            ApiToolProvider.name == req.name.data,
            ApiToolProvider.id != api_tool_provider.id
        ).one_or_none()
        if check_api_tool_provider:
            raise ValidateErrorException(f"该工具提供者名字{req.name.data}已存在")

        # 4.开启数据库的自动提交
        with self.db.auto_commit():
            # 5.先删除该工具提供者下的所有工具
            self.db.session.query(ApiTool).filter(
                ApiTool.provider_id == api_tool_provider.id,
                ApiTool.account_id == account.id,
            ).delete()

        # 6.修改工具提供者信息
        self.update(
            api_tool_provider,
            name=req.name.data,
            icon=req.icon.data,
            headers=req.headers.data,
            openapi_schema=req.openapi_schema.data,
        )

        # 7.新增工具信息从而完成覆盖更新
        for path, path_item in openapi_schema.paths.items():
            for method, method_item in path_item.items():
                self.create(
                    ApiTool,
                    account_id=account.id,
                    provider_id=api_tool_provider.id,
                    name=method_item.get("operationId"),
                    description=method_item.get("description"),
                    url=f"{openapi_schema.server}{path}",
                    method=method,
                    parameters=method_item.get("parameters", []),
                )

    def get_api_tool_providers_with_page(
            self,
            req: GetApiToolProvidersWithPageReq,
            account: Account,
    ) -> tuple[list[Any], Paginator]:
        """获取自定义API工具服务提供者分页列表数据"""
        # 1.构建分页查询器
        paginator = Paginator(db=self.db, req=req)

        # 2.构建筛选器
        filters = [ApiToolProvider.account_id == account.id]
        if req.search_word.data:
            filters.append(ApiToolProvider.name.ilike(f"%{req.search_word.data}%"))

        # 3.执行分页并获取数量
        api_tool_providers = paginator.paginate(
            self.db.session.query(ApiToolProvider).filter(*filters).order_by(desc("created_at")),
        )

        return api_tool_providers, paginator

    def create_api_tool(
            self,
            req: CreateApiToolReq,
            account: Account,
    ) -> None:
        """根据传递的请求创建自定义API工具"""
        # 1.检验并提取openapi_schema对应的数据
        openapi_schema = self.parse_openapi_schema(req.openapi_schema.data)

        # 2.查询当前登录的账号是否已经创建了同名的工具提供者，如果是则抛出异常
        api_tool_provider = self.db.session.query(ApiToolProvider).filter_by(
            account_id=account.id,
            name=req.name.data,
        ).one_or_none()
        if api_tool_provider:
            raise ValidateErrorException(f"该工具提供者名字{req.name.data}已存在")

        # 3.首先创建根据提供者，并获取根据提供者的id信息，然后再创建工具信息
        api_tool_provider = self.create(
            ApiToolProvider,
            account_id=account.id,
            name=req.name.data,
            icon=req.icon.data,
            description=openapi_schema.description,
            openapi_schema=req.openapi_schema.data,
            headers=req.headers.data,
        )

        # 4.创建api工具并关联api_tool_provider
        for path, path_item in openapi_schema.paths.items():
            for method, method_item in path_item.items():
                self.create(
                    ApiTool,
                    account_id=account.id,
                    provider_id=api_tool_provider.id,
                    name=method_item.get("operationId"),
                    description=method_item.get("description"),
                    url=f"{openapi_schema.server}{path}",
                    method=method,
                    parameters=method_item.get("parameters", []),
                )

    def get_api_tool(
            self,
            provider_id: UUID,
            tool_name: str,
            account: Account,
    ) -> ApiTool:
        """根据传递的provider_id + tool_name获取对应工具的详情消息"""
        # TODO:bug
        api_tool = self.db.session.query(ApiTool).filter_by(
            provider_id=provider_id,
            name=tool_name,
        ).one_or_none()

        if api_tool is None or str(api_tool.account_id) != account.id:
            raise NotFoundException("该工具不存在")

        return api_tool

    def delete_api_tool_provider(
            self,
            provider_id: UUID,
            account: Account,
    ):
        """根据传递的provider_name删除对应的工具提供商+工具的所有信息"""
        # 1.先查照数据，检测下provider_id对应的数据是否存在，权限是否正确
        api_tool_provider = self.get(ApiToolProvider, provider_id)
        if api_tool_provider is None or str(api_tool_provider.account_id) != account.id:
            raise NotFoundException("该工具提供者不存在")

        # 2.开启数据库的自动提交
        # TODO:bug
        with self.db.auto_commit():
            # 3.先来删除提供者对应的工具信息
            self.db.session.query(ApiTool).filter(
                ApiTool.provider_id == provider_id,
                ApiTool.account_id == account.id,
            ).delete()

            # 4.删除服务提供商
            self.db.session.delete(api_tool_provider)

        pass

    @classmethod
    def parse_openapi_schema(cls, openapi_schema_str: str) -> OpenAPISchema:
        """解析传递的openapi_schema字符串，如果出错则抛出错误"""
        try:
            data = json.loads(openapi_schema_str.strip())
            if not isinstance(data, dict):
                raise
        except Exception as e:
            raise ValidateErrorException("传递数据必须符合OpenAPI规范的JSON字符串")

        return OpenAPISchema(**data)

    def get_api_tool_provider(
            self,
            provider_id: UUID,
            account: Account,
    ) -> ApiToolProvider:
        """"根据传递的provider_id获取API工具提供者信息"""
        # 1.查询数据库获取对应的数据
        api_tool_provider = self.get(ApiToolProvider, provider_id)

        # 2.校验数据是否为空，并且判断该数据是否属于当且账号
        if api_tool_provider is None or str(api_tool_provider.account_id) != account.id:
            raise NotFoundException("该工具提供者不存在")

        return api_tool_provider

    def api_tool_invoke(self):
        provider_id = "f3f9bd94-7f93-444b-b693-9cbd68d55dde"
        tool_name = "YoudaoSuggest"

        api_tool = self.db.session.query(ApiTool).filter(
            ApiTool.provider_id == provider_id,
            ApiTool.name == tool_name,
        ).one_or_none()
        api_tool_provider = api_tool.provider

        from internal.core.tools.api_tools.entities import ToolEntity
        tool = self.api_provider_manager.get_tool(ToolEntity(
            id=provider_id,
            name=tool_name,
            url=api_tool.url,
            method=api_tool.method,
            description=api_tool.description,
            headers=api_tool_provider.headers,
            parameters=api_tool.parameters,
        ))
        return tool.invoke({"q": "love", "doctype": "json"})