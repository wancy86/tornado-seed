create table if not exists todo_project_group(
/*
项目组表
只有用户属于这个项目，用户才可以查看这个项目的相关信息
*/
    identity int auto_increment,
    userid varchar(36) not null, -- 用户ID
    projectid varchar(36) not null, -- 任务ID

    entry_user varchar(36) not null default '', -- 常规字段: 记录添加人
    entry_date datetime not null default now(), -- 常规字段: 记录添加时间

    key(identity),
    primary key(userid, projectid)
);