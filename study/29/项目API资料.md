# LLMOps 项目 API 文档

应用 API 接口统一以 JSON 格式返回，并且包含 3 个字段：`code`、`data` 和 `message`，分别代表`业务状态码`、`业务数据`和`接口附加信息`。

`业务状态码`共有 6 种，其中只有 `success(成功)` 代表业务操作成功，其他 5 种状态均代表失败，并且失败时会附加相关的信息：`fail(通用失败)`、`not_found(未找到)`、`unauthorized(未授权)`、`forbidden(无权限)`和`validate_error(数据验证失败)`。
