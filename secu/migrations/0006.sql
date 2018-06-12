-- insert into secu_right (id, name, description) values
--   ('600', '日志管理', '日志管理菜单');

-- update secu_role
-- set rights = '100, 101, 102, 103, 200, 201, 202, 203, 300, 301, 302, 303, 400, 401, 402, 403, 600'
-- where name = 'admin';

create table if not exists todo_favorite_item(
/*
我的关注
一个用户可以关注多个item
*/
    id int auto_increment not null,
    userid varchar(36) not null, -- 用户ID
    itemid varchar(36) not null, -- 任务ID

    entry_user varchar(36) not null default '', -- 常规字段: 记录添加人
    entry_date datetime not null default now(), -- 常规字段: 记录添加时间

    primary key(id)
);

