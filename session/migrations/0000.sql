create table if not exists migration(
    app varchar(100) not null,
    version char(4) not null,
    entry_date datetime not null default now(),
    primary key (app, version)
)