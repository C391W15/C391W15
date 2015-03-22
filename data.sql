--
-- Assignment Database 
-- Cody Ingram
--

-- Populate Persons table

insert into persons values (1111, 'Cody', 'Ingram', '123 Sesame St.', 'cdingram@ualberta.ca', '911');

-- Populate Users table

insert into users values ('Cody', 'foo', 'a', 1111, STR_TO_DATE('18-10-1994', '%d-%m-%Y'));
