create table if not exists secu_user(
    id varchar(36) not null,
    username varchar(100) not null default '',
    pwd varchar(100) not null,
    email varchar(100) not null default '',
    mobile varchar(100) not null default '',
    active smallint not null default 0,
    fullname varchar(100) not null default '',
    roles varchar(10000),
    wrongtimes int not null default 0,
    entry_user varchar(36),
    entry_date datetime not null default now(), 
    identity int auto_increment,
    
    key(identity),       
    primary key (id)
); 

create table if not exists secu_role(
    id varchar(36) not null,
    name varchar(100) not null,
    description varchar(10000) null,
    rights varchar(10000) null,
    entry_user varchar(36),
    entry_date datetime not null default now(),   
    identity int auto_increment,
    
    key(identity),      
    primary key (id)
);  

create table if not exists secu_right(
    id varchar(36) not null,
    name varchar(100) not null,
    description varchar(100) null,
    config varchar(100) null,
    entry_user varchar(36),
    entry_date datetime not null default now(),   
    identity int auto_increment,
    
    key(identity),      
    primary key (id)
);    
