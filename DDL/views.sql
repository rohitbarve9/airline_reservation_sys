drop view if exists show_jobs;
drop view if exists show_options;
drop view if exists show_trips;
drop trigger if exists is_full_flag;
drop trigger if exists pilot_present;
drop trigger if exists set_full_seat;
drop function if exists busy_pilot;
drop function if exists popular_dest;
drop function if exists loyal_customer;
drop procedure if exists add_customer;
drop procedure if exists add_pilot;
drop procedure if exists add_flight;
drop procedure if exists add_trip;
drop procedure if exists add_job;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW `show_jobs` AS select `pf`.`flight_num` AS `flight_num`,`f`.`airline` AS
`airline`,`f`.`depart_airport` AS `depart_airport`,`f`.`arrive_airport` AS `arrive_airport`,`pf`.`pilot_num`
AS `pilot_num` from (`pilots_flight` `pf` left join `flight` `f` on((`pf`.`flight_num` = `f`.`flight_num`)));

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW `show_options` AS select `flight`.`flight_num` AS `flight_num`,`flight`.`depart_airport` AS
`depart_airport`,`flight`.`arrive_airport` AS `arrive_airport`,`flight`.`is_full` AS
`is_full`,`flight`.`has_pilot` AS `has_pilot` from `flight`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW `show_trips` AS select `trip`.`trip_id` AS `trip_id`,`trip`.`flight_num` AS
`flight_num`,`trip`.`depart_airport` AS `depart_airport`,`trip`.`arrive_airport` AS `arrive_airport`,`trip`.`customer_id` AS `customer_id` from
`trip`;

DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `busy_pilot`() RETURNS varchar(20) CHARSET
utf8mb4
DETERMINISTIC
begin
declare busy_pilot varchar(15);
select pilot_name into busy_pilot from pilot
where pilot_num = (select pilot_num from pilots_flight group by pilot_num order by
count(pilot_num) desc limit 1);
return busy_pilot;
end; //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `popular_dest`() RETURNS varchar(15)
CHARSET utf8mb4
DETERMINISTIC
begin
declare popular_dest varchar(15);
select arrive_airport into popular_dest
from trip
group by arrive_airport
order by count(arrive_airport) desc
limit 1;
return popular_dest;
end; //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `loyal_customer`() RETURNS varchar(15)
CHARSET utf8mb4
DETERMINISTIC
begin
declare loyal_customer varchar(15);
select customer_name into loyal_customer
from customer where customer_id = (select customer_id from trip group by customer_id
order by count(customer_id) desc limit 1);
return loyal_customer;
end; //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` TRIGGER `pilot_present` AFTER INSERT ON `pilots_flight`
FOR EACH ROW
begin
update flight 
set has_pilot = 1
where flight.flight_num = new.flight_num;
end; //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE add_customer
(IN customer_id varchar(15),IN customer_name varchar(20),IN gender varchar(10),
IN address varchar(40),IN city varchar(20),IN state varchar(20),IN zip varchar(20),
IN date_of_birth varchar(10),IN age numeric(2,0),IN phone_number numeric(10,0))
BEGIN
START TRANSACTION;
INSERT INTO customer(customer_id,customer_name,gender,address,city,state,zip,date_of_birth,age,phone_number) VALUES (customer_id,customer_name,gender,address,city,state,zip,date_of_birth,age,phone_number);
COMMIT;
END; //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE add_pilot
(IN pilot_num varchar(15),IN pilot_name varchar(20),IN airline varchar(15),IN gender varchar(10),
IN address varchar(40),IN city varchar(20),IN state varchar(20),IN zip varchar(20),
IN date_of_birth varchar(10),IN age numeric(2,0),IN phone_number numeric(10,0))
BEGIN
START TRANSACTION;
INSERT INTO pilot(pilot_num,pilot_name,airline,gender,address,city,state,zip,date_of_birth,age,phone_number) VALUES (pilot_num,pilot_name,airline,gender,address,city,state,zip,date_of_birth,age,phone_number);
COMMIT;
END; //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE add_flight
(IN flight_num varchar(15),IN plane_type varchar(15),IN airline varchar(15),IN depart_airport varchar(15),
IN arrive_airport varchar(15),IN depart_gate varchar(15),IN arrive_gate varchar(15))
BEGIN
START TRANSACTION;
INSERT INTO flight(flight_num,plane_type,airline,depart_airport,arrive_airport,depart_gate,arrive_gate) VALUES (flight_num,plane_type,airline,depart_airport,arrive_airport,depart_gate,arrive_gate);
COMMIT;
END; //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE add_trip
(IN depart_airport varchar(15), IN arrive_airport varchar(15),IN customer_id varchar(15),IN flight_num varchar(15),
IN trip_id varchar(15), IN seat_num varchar(15))
BEGIN
START TRANSACTION;
INSERT INTO trip(depart_airport, arrive_airport, customer_id, flight_num, trip_id, seat_num) VALUES (depart_airport, arrive_airport, customer_id, flight_num, trip_id, seat_num);
COMMIT;
END; //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE add_job
(IN pilot_num varchar(15), IN flight_num varchar(15))
BEGIN
INSERT INTO pilots_flight(pilot_num, flight_num) VALUES (pilot_num, flight_num);
END; //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` TRIGGER `is_full_flag` AFTER INSERT ON `trip` 
FOR EACH ROW 
begin
update flight 
set is_full = 1
where flight.max_seats <= (select count(*) 
from trip 
where trip.flight_num = NEW.flight_num);
end; //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` TRIGGER `set_full_seat` AFTER INSERT ON `trip` 
FOR EACH ROW 
begin
update seat 
set is_booked = 1
where seat.seat_num = NEW.flight_num
AND seat.flight_num = NEW.flight_num;
end; //
DELIMITER ;




















