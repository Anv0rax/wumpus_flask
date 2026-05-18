create sequence user_table_id_seq
    as integer;

alter sequence user_table_id_seq owner to py13;

create sequence players_table_id_seq
    as integer;

alter sequence players_table_id_seq owner to py13;

alter sequence players_table_id_seq owned by user_table.id;









create table user_table
(
    id                integer default nextval('players_table_id_seq'::regclass) not null
        constraint players_table_pkey
            primary key,
    username          varchar(50)                                               not null
        constraint players_table_username_key
            unique,
    pwd_hash          text                                                      not null,
    icon              text,
    score             integer default 0                                         not null,
    numberofvictories integer default 0                                         not null,
    defeats           integer default 0,
    fell_slime_pit    integer default 0,
    missed            integer default 0                                         not null,
    bat_touched       integer default 0                                         not null
);

alter table user_table
    owner to py13;

