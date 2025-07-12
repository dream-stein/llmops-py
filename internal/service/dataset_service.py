#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/12 15:31
#Author  :Emcikem
@File    :dataset_service.py
"""
from uuid import UUID

from sqlalchemy import desc

from internal.service import BaseService
from injector import inject
from dataclasses import dataclass

from pkg.paginator import Paginator
from internal.exception import ValidateErrorException
from internal.model import Dataset

from pkg.sqlalchemy import SQLAlchemy
from internal.schema.dataset_schema import CreateDatasetReq, UpdateDatasetReq, GetDatasetsWithPageReq
from internal.entity.dataset_entity import DEFAULT_DATASET_DESCRIPTION_FORMATTER
from internal.exception import NotFoundException


@inject
@dataclass
class DatasetService(BaseService):
    """知识库服务"""
    db: SQLAlchemy

    def create_dataset(self, req: CreateDatasetReq) -> Dataset:
        """根据传递的请求信息创建知识库"""
        # todo:等待授权认证模块
        account_id = "b8434b9c-ee56-4bfd-bd24-84d3caef5599"

        # 1.检索该账号下是否存在同名知识库
        datasets = self.db.session.query(Dataset).filter_by(
            account_id=account_id,
            name=req.name,
        ).one_or_none()
        if datasets:
            raise ValidateErrorException(f"该知识库{req.name.data}已存在")

        # 2.检测是否传递了描述信息，如果没有就补充
        if req.description.data is None or req.description.data.strip() == "":
            req.description.data = DEFAULT_DATASET_DESCRIPTION_FORMATTER.format(name=req.name.data)

        # 3.创建知识库记录并返回
        return self.create(
            Dataset,
            account_id=account_id,
            name=req.name.data,
            icon=req.icon.data,
            description=req.description.data,
        )

    def get_dataset(self, dataset_id: UUID) -> Dataset:
        """根据传递的知识库id获取知识库记录"""
        # todo:等待授权认证模块
        account_id = "b8434b9c-ee56-4bfd-bd24-84d3caef5599"

        dataset = self.get(Dataset, dataset_id)
        if dataset is None or str(dataset.account_id) != account_id:
            raise NotFoundException("该知识库不存在")

        return dataset

    def update_dataset(self, dataset_id: UUID, req: UpdateDatasetReq) -> Dataset:
        """根据传递的知识库id+数据更新数据库"""

        # todo:等待授权认证模块
        account_id = "b8434b9c-ee56-4bfd-bd24-84d3caef5599"

        # 1.检测知识库是否存在，并且校验
        dataset = self.get(Dataset, dataset_id)
        if dataset is None or str(dataset.account_id) != account_id:
            raise NotFoundException("该知识库不存在")

        # 2.检测修改后的知识库是否出现重名
        check_dataset = self.db.session.query(Dataset).filter(
            Dataset.account_id == account_id,
            Dataset.name == req.name.data,
            Dataset.id != dataset.id,
        ).one_or_none()
        if check_dataset:
            raise ValidateErrorException(f"该知识库名称:{req.name.data}已存在，请修改")

        # 3.校验描述信息是否为空，如果为空则人为设置
        if req.description.data is None or req.description.data.strip() == "":
            req.description.data = DEFAULT_DATASET_DESCRIPTION_FORMATTER.format(name=req.name.data)

        # 4.更新数据
        self.update(
            dataset,
            name=req.name.data,
            icon=req.icon.data,
            description=req.description.data,
        )

        return dataset

    def get_datasets_with_page(self, req: GetDatasetsWithPageReq) -> tuple[list[Dataset], Paginator]:
        """根据传递的信息获取知识库列表分页数据"""
        # todo:等待授权认证模块
        account_id = "b8434b9c-ee56-4bfd-bd24-84d3caef5599"

        # 1.构建分页查询器
        paginator = Paginator(db=self.db, req=req)

        # 2.构建筛选器
        filters = [Dataset.account_id == account_id]
        if req.search_word.data:
            filters.append(Dataset.name.ilike(f"%{req.search_word.data}%"))

        # 3.执行分页并获取数据
        datasets = paginator.paginate(
            self.db.session.query(Dataset).filter(*filters).order_by(desc("created_at")),
        )

        return datasets, paginator