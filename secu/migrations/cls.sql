set foreign_key_checks = 0;

delete from session;
delete from session_data; 

delete from secu_user;
delete from secu_role;

delete from todo_project;
delete from todo_item;
delete from todo_person_in_charge;
delete from todo_work;
delete from todo_project_group;    
    
set foreign_key_checks = 1;