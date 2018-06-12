/*
总体说明：
1. 所有加了tablename$格式的表格，都表示为日志记录表
2. 所有的varchar(36)都代表了GUID，如0fcddadb30854f30936aeb9fac3ec4e6
3. 所有的char(36)的数据分为两部分，前3位留作备用，默认为000；
   后32位作为唯一标识，例如000-0fcddadb30854f30936aeb9fac3ec4e6
*/


create table if not exists todo_project(
/*
项目表，更新时会将首先原封不动拷贝一条记录到history记录里面，然后再做update操作
*/
    id varchar(36) not null, -- unique id
    name varchar(100) not null, -- 项目名称
    desp varchar(10000) not null, -- 项目介绍
    cats varchar(1000) not null default '', -- 任务类别|数据格式为JSON: 如['需求', '缺陷']
    statuses varchar(1000) not null default '', -- 任务状态|数据格式为JSON: 如['尚未分配', '已分配', '开发中', '开发完成', '测试中', '测试完成', '已验收']
    priorities varchar(1000) not null default '', -- 任务优先级|JSON数据格式：如['高', '中', '低']

    entry_user varchar(36) not null default '', -- 常规字段: 记录添加人
    entry_date datetime not null default now(), -- 常规字段: 记录添加时间
    identity int auto_increment,

    key(identity),
    primary key(id)
);

create table if not exists todo_project$(
    id varchar(36) not null, -- unique id
    name varchar(100) not null, -- 项目名称
    desp varchar(10000) not null, -- 项目介绍
    cats varchar(1000) not null default '', -- 任务类别|数据格式为JSON: 如['需求', '缺陷']
    statuses varchar(1000) not null default '', -- 任务状态|数据格式为JSON: 如['开发', '评审', '测试', '验收']
    priorities varchar(1000) not null default '', -- 任务优先级|JSON数据格式：如['高', '中', '低']

    entry_user varchar(36) not null, -- 常规字段: 记录添加人
    entry_date datetime not null, -- 常规字段: 记录添加时间
    identity int auto_increment,

    key(identity),
    primary key(id)
);

create table if not exists todo_item(
/*
待办事项表
*/
    id varchar(36) not null, -- unique id
    projectid varchar(36) not null,
    title varchar(255) not null, -- 任务名称
    desp varchar(10000) not null, -- 任务描述
    cat varchar(100), -- 任务类别
    status varchar(100), -- 当前任务状态
    priority varchar(100), -- 任务优先级
    estimated_duration int, -- 预估消耗时间，单位分钟

    entry_user varchar(36) not null default '', -- 常规字段: 记录添加人
    entry_date datetime not null default now(), -- 常规字段: 记录添加时间
    identity int auto_increment,

    key(identity),
    primary key(id)
);

create table if not exists todo_item$(
/*
待办事项表，结算完成后不可添加工作记录
*/
    id varchar(36) not null, -- unique id
    projectid varchar(36) not null,
    title varchar(255) not null, -- 任务名称
    desp varchar(10000) not null, -- 任务描述
    cat varchar(100), -- 任务类别
    status varchar(100), -- 当前任务状态
    priority varchar(100), -- 任务优先级
    estimated_duration int, -- 预估消耗时间，单位分钟

    entry_user varchar(36) not null default '', -- 常规字段: 记录添加人
    entry_date datetime not null default now(), -- 常规字段: 记录添加时间
    identity int auto_increment,

    key(identity),
    primary key(id)
);


create table if not exists todo_person_in_charge(
/*
待办事项表，结算完成后不可添加工作记录
*/
    itemid varchar(36) not null, -- 任务ID
    itemstatus varchar(100) not null, -- 任务状态
    person_in_charge varchar(36) not null, -- 任务负责人
    sequence int not null default 0,

    entry_user varchar(36) not null default '', -- 常规字段: 记录添加人
    entry_date datetime not null default now(), -- 常规字段: 记录添加时间
    identity int auto_increment,

    key(identity),
    primary key(itemid, itemstatus)
);

create table if not exists todo_person_in_charge$(
/*
待办事项表，结算完成后不可添加工作记录
*/
    itemid varchar(36) not null, -- 任务ID
    itemstatus varchar(100) not null, -- 任务状态
    person_in_charge varchar(36) not null, -- 任务负责人
    sequence int not null default 0,

    entry_user varchar(36) not null default '', -- 常规字段: 记录添加人
    entry_date datetime not null default now(), -- 常规字段: 记录添加时间
    identity int auto_increment,

    key(identity),
    primary key(itemid, itemstatus)
);

create table if not exists todo_work(
/*
工作日志表，消耗时间填写1个小时后不可改动，结算完成后不可改动
*/
    id varchar(36) not null, -- unique id
    itemid varchar(36) not null, -- 任务ID
    desp varchar(10000), -- 工作内容
    duration int comment 'name="消耗时间", maxvalue=480, message="不符合规则(0-480)"', 
    entry_user varchar(36) not null default '', -- 常规字段: 记录添加人
    entry_date datetime not null default now(), -- 常规字段: 记录添加时间
    identity int auto_increment,

    key(identity),
    primary key(id)
);