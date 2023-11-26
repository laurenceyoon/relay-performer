PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE pieces (
	id INTEGER NOT NULL, 
	title VARCHAR, 
	path VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO pieces VALUES(1,'cmaj','./resources/midi/full/cmaj.mid');
INSERT INTO pieces VALUES(2,'Haydn_Hob._XVI34_1._Presto','./resources/midi/full/Haydn_Hob._XVI34_1._Presto.mid');
INSERT INTO pieces VALUES(3,'Haydn_Hob._XVI34_2.Adagio','./resources/midi/full/Haydn_Hob._XVI34_2.Adagio.mid');
INSERT INTO pieces VALUES(4,'Haydn_Hob._XVI34_3.Molto_Vivace','./resources/midi/full/Haydn_Hob._XVI34_3.Molto_Vivace.mid');
INSERT INTO pieces VALUES(5,'Ave Maria','../resources/midi/full/avemaria.mid');
CREATE TABLE subpieces (
	id INTEGER NOT NULL, 
	title VARCHAR, 
	path VARCHAR, 
	piece_id INTEGER, 
	etr FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(piece_id) REFERENCES pieces (id)
);
INSERT INTO subpieces VALUES(1,'Haydn_Hob.XVI34_1-1','./resources/midi/subpieces/Haydn_Hob.XVI34_1-1.mid',2,0.0);
INSERT INTO subpieces VALUES(2,'Haydn_Hob.XVI34_1-2','./resources/midi/subpieces/Haydn_Hob.XVI34_1-2.mid',2,0.0);
INSERT INTO subpieces VALUES(3,'Haydn_Hob.XVI34_1-3','./resources/midi/subpieces/Haydn_Hob.XVI34_1-3.mid',2,0.0);
INSERT INTO subpieces VALUES(4,'Haydn_Hob.XVI34_1-4','./resources/midi/subpieces/Haydn_Hob.XVI34_1-4.mid',2,0.0);
INSERT INTO subpieces VALUES(5,'Haydn_Hob.XVI34_1-5','./resources/midi/subpieces/Haydn_Hob.XVI34_1-5.mid',2,0.0);
INSERT INTO subpieces VALUES(6,'Haydn_Hob.XVI34_1-6','./resources/midi/subpieces/Haydn_Hob.XVI34_1-6.mid',2,0.0);
INSERT INTO subpieces VALUES(7,'Haydn_Hob.XVI34_1-7','./resources/midi/subpieces/Haydn_Hob.XVI34_1-7.mid',2,0.0);
INSERT INTO subpieces VALUES(8,'Haydn_Hob.XVI34_1-8','./resources/midi/subpieces/Haydn_Hob.XVI34_1-8.mid',2,0.0);
INSERT INTO subpieces VALUES(9,'Haydn_Hob.XVI34_1-9','./resources/midi/subpieces/Haydn_Hob.XVI34_1-9.mid',2,0.0);
INSERT INTO subpieces VALUES(10,'Haydn_Hob.XVI34_1-10','./resources/midi/subpieces/Haydn_Hob.XVI34_1-10.mid',2,0.0);
INSERT INTO subpieces VALUES(11,'Haydn_Hob.XVI34_1-11','./resources/midi/subpieces/Haydn_Hob.XVI34_1-11.mid',2,0.0);
INSERT INTO subpieces VALUES(12,'Haydn_Hob.XVI34_1-12','./resources/midi/subpieces/Haydn_Hob.XVI34_1-12.mid',2,0.0);
INSERT INTO subpieces VALUES(13,'Haydn_Hob.XVI34_1-13','./resources/midi/subpieces/Haydn_Hob.XVI34_1-13.mid',2,0.0);
INSERT INTO subpieces VALUES(14,'Haydn_Hob.XVI34_1-14','./resources/midi/subpieces/Haydn_Hob.XVI34_1-14.mid',2,0.0);
INSERT INTO subpieces VALUES(15,'Haydn_Hob.XVI34_1-15','./resources/midi/subpieces/Haydn_Hob.XVI34_1-15.mid',2,0.0);
INSERT INTO subpieces VALUES(16,'Haydn_Hob.XVI34_1-16','./resources/midi/subpieces/Haydn_Hob.XVI34_1-16.mid',2,0.0);
INSERT INTO subpieces VALUES(17,'Haydn_Hob.XVI34_1-17','./resources/midi/subpieces/Haydn_Hob.XVI34_1-17.mid',2,0.0);
INSERT INTO subpieces VALUES(18,'Haydn_Hob.XVI34_1-18','./resources/midi/subpieces/Haydn_Hob.XVI34_1-18.mid',2,0.0);
INSERT INTO subpieces VALUES(19,'Haydn_Hob.XVI34_1-19','./resources/midi/subpieces/Haydn_Hob.XVI34_1-19.mid',2,0.0);
INSERT INTO subpieces VALUES(20,'Haydn_Hob.XVI34_2-1','./resources/midi/subpieces/Haydn_Hob.XVI34_2-1.mid',3,0.9);
INSERT INTO subpieces VALUES(21,'Haydn_Hob.XVI34_2-2','./resources/midi/subpieces/Haydn_Hob.XVI34_2-2.mid',3,0.0);
INSERT INTO subpieces VALUES(22,'Haydn_Hob.XVI34_2-3','./resources/midi/subpieces/Haydn_Hob.XVI34_2-3.mid',3,0.9);
INSERT INTO subpieces VALUES(23,'Haydn_Hob.XVI34_2-4','./resources/midi/subpieces/Haydn_Hob.XVI34_2-4.mid',3,0.0);
INSERT INTO subpieces VALUES(24,'Haydn_Hob.XVI34_2-5','./resources/midi/subpieces/Haydn_Hob.XVI34_2-5.mid',3,0.9);
INSERT INTO subpieces VALUES(25,'Haydn_Hob.XVI34_2-6','./resources/midi/subpieces/Haydn_Hob.XVI34_2-6.mid',3,0.0);
INSERT INTO subpieces VALUES(26,'Haydn_Hob.XVI34_2-7','./resources/midi/subpieces/Haydn_Hob.XVI34_2-7.mid',3,1.5);
INSERT INTO subpieces VALUES(27,'Haydn_Hob.XVI34_2-8','./resources/midi/subpieces/Haydn_Hob.XVI34_2-8.mid',3,0.0);
INSERT INTO subpieces VALUES(28,'Haydn_Hob.XVI34_2-9','./resources/midi/subpieces/Haydn_Hob.XVI34_2-9.mid',3,1.7);
INSERT INTO subpieces VALUES(29,'Haydn_Hob.XVI34_2-10','./resources/midi/subpieces/Haydn_Hob.XVI34_2-10.mid',3,0.0);
INSERT INTO subpieces VALUES(30,'Haydn_Hob.XVI34_2-11','./resources/midi/subpieces/Haydn_Hob.XVI34_2-11.mid',3,0.0);
INSERT INTO subpieces VALUES(31,'Haydn_Hob.XVI34_2-12','./resources/midi/subpieces/Haydn_Hob.XVI34_2-12.mid',3,0.0);
INSERT INTO subpieces VALUES(32,'Haydn_Hob.XVI34_2-13','./resources/midi/subpieces/Haydn_Hob.XVI34_2-13.mid',3,0.0);
INSERT INTO subpieces VALUES(33,'Haydn_Hob.XVI34_2-14','./resources/midi/subpieces/Haydn_Hob.XVI34_2-14.mid',3,0.0);
INSERT INTO subpieces VALUES(34,'Haydn_Hob.XVI34_2-15','./resources/midi/subpieces/Haydn_Hob.XVI34_2-15.mid',3,0.0);
INSERT INTO subpieces VALUES(35,'Haydn_Hob.XVI34_3-1','./resources/midi/subpieces/Haydn_Hob.XVI34_3-1.mid',4,0.0);
INSERT INTO subpieces VALUES(36,'Haydn_Hob.XVI34_3-2','./resources/midi/subpieces/Haydn_Hob.XVI34_3-2.mid',4,1.1000000000000000888);
INSERT INTO subpieces VALUES(37,'Haydn_Hob.XVI34_3-3','./resources/midi/subpieces/Haydn_Hob.XVI34_3-3.mid',4,0.0);
INSERT INTO subpieces VALUES(38,'Haydn_Hob.XVI34_3-4','./resources/midi/subpieces/Haydn_Hob.XVI34_3-4.mid',4,1.1000000000000000888);
INSERT INTO subpieces VALUES(39,'Haydn_Hob.XVI34_3-5','./resources/midi/subpieces/Haydn_Hob.XVI34_3-5.mid',4,0.0);
INSERT INTO subpieces VALUES(40,'Haydn_Hob.XVI34_3-6','./resources/midi/subpieces/Haydn_Hob.XVI34_3-6.mid',4,1.3999999999999999111);
INSERT INTO subpieces VALUES(41,'Haydn_Hob.XVI34_3-7','./resources/midi/subpieces/Haydn_Hob.XVI34_3-7.mid',4,0.0);
INSERT INTO subpieces VALUES(42,'Haydn_Hob.XVI34_3-8','./resources/midi/subpieces/Haydn_Hob.XVI34_3-8.mid',4,4.0);
INSERT INTO subpieces VALUES(43,'Haydn_Hob.XVI34_3-9','./resources/midi/subpieces/Haydn_Hob.XVI34_3-9.mid',4,0.0);
INSERT INTO subpieces VALUES(44,'Haydn_Hob.XVI34_3-10','./resources/midi/subpieces/Haydn_Hob.XVI34_3-10.mid',4,1.1000000000000000888);
INSERT INTO subpieces VALUES(45,'Haydn_Hob.XVI34_3-11','./resources/midi/subpieces/Haydn_Hob.XVI34_3-11.mid',4,0.0);
INSERT INTO subpieces VALUES(46,'Haydn_Hob.XVI34_3-12','./resources/midi/subpieces/Haydn_Hob.XVI34_3-12.mid',4,1.1000000000000000888);
INSERT INTO subpieces VALUES(47,'Haydn_Hob.XVI34_3-13','./resources/midi/subpieces/Haydn_Hob.XVI34_3-13.mid',4,0.0);
INSERT INTO subpieces VALUES(48,'Haydn_Hob.XVI34_3-14','./resources/midi/subpieces/Haydn_Hob.XVI34_3-14.mid',4,1.1999999999999999644);
INSERT INTO subpieces VALUES(49,'Haydn_Hob.XVI34_3-15','./resources/midi/subpieces/Haydn_Hob.XVI34_3-15.mid',4,0.0);
INSERT INTO subpieces VALUES(50,'Haydn_Hob.XVI34_3-16','./resources/midi/subpieces/Haydn_Hob.XVI34_3-16.mid',4,1.1000000000000000888);
INSERT INTO subpieces VALUES(51,'Haydn_Hob.XVI34_3-17','./resources/midi/subpieces/Haydn_Hob.XVI34_3-17.mid',4,0.0);
INSERT INTO subpieces VALUES(52,'Haydn_Hob.XVI34_3-18','./resources/midi/subpieces/Haydn_Hob.XVI34_3-18.mid',4,1.0);
INSERT INTO subpieces VALUES(53,'Haydn_Hob.XVI34_3-19','./resources/midi/subpieces/Haydn_Hob.XVI34_3-19.mid',4,0.0);
INSERT INTO subpieces VALUES(54,'Ave Maria 1','./resources/midi/subpieces/avemaria_1.mid',5,0.0);
INSERT INTO subpieces VALUES(55,'Ave Maria 2','./resources/midi/subpieces/avemaria_2.mid',5,0.0);
CREATE TABLE schedules (
	id INTEGER NOT NULL, 
	start_measure INTEGER, 
	end_measure INTEGER, 
	player VARCHAR, 
	piece_id INTEGER, 
	subpiece_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(piece_id) REFERENCES pieces (id), 
	FOREIGN KEY(subpiece_id) REFERENCES subpieces (id)
);
INSERT INTO schedules VALUES(1,1,8,'Pianist',2,1);
INSERT INTO schedules VALUES(2,9,29,'VirtuosoNet',2,2);
INSERT INTO schedules VALUES(3,30,35,'Pianist',2,3);
INSERT INTO schedules VALUES(4,36,53,'VirtuosoNet',2,4);
INSERT INTO schedules VALUES(5,54,74,'Pianist',2,5);
INSERT INTO schedules VALUES(6,75,80,'VirtuosoNet',2,6);
INSERT INTO schedules VALUES(7,81,90,'Pianist',2,7);
INSERT INTO schedules VALUES(8,91,95,'VirtuosoNet',2,8);
INSERT INTO schedules VALUES(9,96,123,'Pianist',2,9);
INSERT INTO schedules VALUES(10,124,139,'VirtuosoNet',2,10);
INSERT INTO schedules VALUES(11,140,145,'Pianist',2,11);
INSERT INTO schedules VALUES(12,146,153,'VirtuosoNet',2,12);
INSERT INTO schedules VALUES(13,154,177,'Pianist',2,13);
INSERT INTO schedules VALUES(14,178,190,'VirtuosoNet',2,14);
INSERT INTO schedules VALUES(15,190,221,'Pianist',2,15);
INSERT INTO schedules VALUES(16,222,227,'VirtuosoNet',2,16);
INSERT INTO schedules VALUES(17,228,235,'Pianist',2,17);
INSERT INTO schedules VALUES(18,236,240,'VirtuosoNet',2,18);
INSERT INTO schedules VALUES(19,241,254,'Pianist',2,19);
INSERT INTO schedules VALUES(20,1,4,'Pianist',3,20);
INSERT INTO schedules VALUES(21,5,8,'VirtuosoNet',3,21);
INSERT INTO schedules VALUES(22,8,18,'Pianist',3,22);
INSERT INTO schedules VALUES(23,18,24,'VirtuosoNet',3,23);
INSERT INTO schedules VALUES(24,25,28,'Pianist',3,24);
INSERT INTO schedules VALUES(25,28,32,'VirtuosoNet',3,25);
INSERT INTO schedules VALUES(26,33,40,'Pianist',3,26);
INSERT INTO schedules VALUES(27,41,44,'VirtuosoNet',3,27);
INSERT INTO schedules VALUES(28,45,51,'Pianist',3,28);
INSERT INTO schedules VALUES(29,52,55,'VirtuosoNet',3,29);
INSERT INTO schedules VALUES(30,56,65,'Pianist',3,30);
INSERT INTO schedules VALUES(31,65,66,'VirtuosoNet',3,31);
INSERT INTO schedules VALUES(32,66,66,'Pianist',3,32);
INSERT INTO schedules VALUES(33,66,67,'VirtuosoNet',3,33);
INSERT INTO schedules VALUES(34,67,69,'Pianist',3,34);
INSERT INTO schedules VALUES(35,1,8,'VirtuosoNet',4,35);
INSERT INTO schedules VALUES(36,8,16,'Pianist',4,36);
INSERT INTO schedules VALUES(37,16,26,'VirtuosoNet',4,37);
INSERT INTO schedules VALUES(38,26,36,'Pianist',4,38);
INSERT INTO schedules VALUES(39,36,44,'VirtuosoNet',4,29);
INSERT INTO schedules VALUES(40,44,52,'Pianist',4,40);
INSERT INTO schedules VALUES(41,52,66,'VirtuosoNet',4,41);
INSERT INTO schedules VALUES(42,66,88,'Pianist',4,42);
INSERT INTO schedules VALUES(43,88,98,'VirtuosoNet',4,43);
INSERT INTO schedules VALUES(44,98,116,'Pianist',4,44);
INSERT INTO schedules VALUES(45,116,124,'VirtuosoNet',4,45);
INSERT INTO schedules VALUES(46,124,132,'Pianist',4,46);
INSERT INTO schedules VALUES(47,132,148,'VirtuosoNet',4,47);
INSERT INTO schedules VALUES(48,148,164,'Pianist',4,48);
INSERT INTO schedules VALUES(49,164,172,'VirtuosoNet',4,49);
INSERT INTO schedules VALUES(50,172,180,'Pianist',4,50);
INSERT INTO schedules VALUES(51,180,190,'VirtuosoNet',4,51);
INSERT INTO schedules VALUES(52,190,198,'Pianist',4,52);
INSERT INTO schedules VALUES(53,199,200,'VirtuosoNet',4,53);
INSERT INTO schedules VALUES(54,0,4,'Pianist',5,54);
INSERT INTO schedules VALUES(55,5,16,'VirtuosoNet',5,55);
CREATE INDEX ix_pieces_id ON pieces (id);
CREATE INDEX ix_pieces_title ON pieces (title);
CREATE INDEX ix_subpieces_id ON subpieces (id);
CREATE INDEX ix_schedules_end_measure ON schedules (end_measure);
CREATE INDEX ix_schedules_id ON schedules (id);
CREATE INDEX ix_schedules_start_measure ON schedules (start_measure);
COMMIT;
