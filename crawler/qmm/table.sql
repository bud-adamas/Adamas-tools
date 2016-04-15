-- file info, from SRC attribute in IMG tag
create table file_info(
    sha1sum     varchar(50),    -- checksum
    source      varchar(100),   -- the url source
    title       varchar(40),    -- the file name
    time        timestamp       -- the time to get
);
create index file_info_sha1sum on file_info(sha1sum);

-- file description, from ALT attribute in IMG tag
create table file_desc(
    sha1sum         varchar(50),    -- checksum
    description     varchar(100)    -- the ALT attribute
);
create index file_desc_description on file_desc(description);
