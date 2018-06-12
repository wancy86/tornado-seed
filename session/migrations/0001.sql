/* table begin */
create table session (
    id varchar(36) not null,
    update_date datetime,
    keep_time int,
    entry_date datetime not null default now(),    
    primary key (id)
);

create table session_data (
    id int not null auto_increment,
    session_id varchar(36) default null,
    k varchar(8000) default null,
    v varchar(8000) default null,
    entry_date datetime default null,
    primary key (id)
);
alter table session_data add constraint fk_session_data_session_id foreign key (session_id) references session (id);

/* table end */