-- file info, from SRC attribute in IMG tag
create table file_info(
    sha1sum     varchar(50)    -- checksum
        PRIMARY KEY,
    source      varchar(100),   -- the url source
    title       varchar(40),    -- the file name
    time        timestamp       -- the time to get
        NOT NULL DEFAULT (datetime('now','localtime'))
);

-- file description, from ALT attribute in IMG tag
create table file_desc(
    sha1sum         varchar(50)    -- checksum
        PRIMARY KEY,
    description     varchar(100)    -- the ALT attribute
);
