# 初始化用户
insert into secu_user (id, mobile, pwd, roles) values
  ('ec7ea5f64fe94018b37f2d942650246c', '13000000000', '000000', '08d1a53842cc4b76be9c187d0f709315');

# 初始化权限列表
insert into secu_right (id, name, description) values
  ('100', '项目管理', '项目管理菜单'),
  ('101', '添加项目', ''),
  ('102', '编辑项目', ''),
  ('103', '删除项目', ''),
  ('200', '任务管理', '任务管理菜单'),
  ('201', '创建任务', ''),
  ('202', '编辑任务', ''),
  ('203', '删除任务', ''),
  ('300', '用户管理', '用户管理菜单'),
  ('301', '添加用户', ''),
  ('302', '编辑用户', ''),
  ('303', '删除用户', ''),
  ('400', '角色管理', '角色管理菜单'),
  ('401', '添加角色', ''),
  ('402', '编辑角色', ''),
  ('403', '删除角色', '');

insert into secu_role (id, name, description, rights)values
('08d1a53842cc4b76be9c187d0f709315', 'admin', 'admin', '100, 101, 102, 103, 200, 201, 202, 203, 300, 301, 302, 303, 400, 401, 402, 403');

-- create table if not exists secu_right(
--     id varchar(36) not null,
--     name varchar(100) not null,
--     description varchar(100) null,
--     config varchar(100) null,
--     entry_user varchar(36),
--     entry_date datetime not null default now(),   
--     identity int auto_increment,

--     key(identity),      
--     primary key (id)
-- );    


