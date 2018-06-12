from secu.controls.__ueditor__ import _Ueditor
from secu.controls.todo_favorite_item import FavoriteItemHandler
from secu.controls.todo_underway import UnderwayHandler
from .controls.secu_login import LoginHandler
from .controls.todo_project import ProjectHandler
from .controls.todo_item import ItemHandler
from .controls.secu_user import UserHandler
from .controls.secu_role import RoleHandler
from .controls.todo_work import WorkHandler
from .controls.todo_project_group import ProjectGroupHandler

urlpatterns = [
    # 登陆: post('mobile', 'pwd')
    (r'/service/secu/login', LoginHandler),

    # 项目接口
    (r'/service/secu/project', ProjectHandler),

    # 任务接口
    (r'/service/secu/item', ItemHandler),

    # 工作内容接口
    (r'/service/secu/work', WorkHandler),

    # 用户管理接口
    (r'/service/secu/user', UserHandler),

    # 角色管理接口
    (r'/service/secu/role', RoleHandler),

    # 进行中的任务
    (r'/service/secu/underway', UnderwayHandler),

    # 项目组
    (r'/service/secu/project-group', ProjectGroupHandler),

    # 关注的任务
    (r'/service/secu/favorite_item', FavoriteItemHandler),

    (r'/service/secu/ueditor', _Ueditor),
]

'''
JSONResponse基本结构：
{
    "code":"\d{3}",
    "msg": "message",
    "data": [] or {}
}

code通用规则：
    0\d\d：其中000表示请求成功，其它的情况表示非预期的请求失败
    1\d\d：验证不通过
    2\d\d：200表示session过期, 201表示窃取CSRF攻击
    5\d\d：表示服务器内部错误
'''
