create table if not exists todo_underway(
/*
进行中的item
*/
    itemid varchar(36) not null, -- 任务ID
    userid varchar(36) not null, -- 任务负责人

    entry_user varchar(36) not null default '', -- 常规字段: 记录添加人
    entry_date datetime not null default now(), -- 常规字段: 记录添加时间
    identity int auto_increment,

    key(identity),
    primary key(itemid, userid)
);