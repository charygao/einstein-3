-- update einstein database
USE einstein;

-- update dbheatpump
ALTER TABLE dbheatpump ADD COLUMN Reference VARCHAR(200) DEFAULT NULL AFTER HPSubType;
ALTER TABLE dbheatpump DROP DBFuel_id;
ALTER TABLE dbheatpump ADD COLUMN FuelType VARCHAR(45) DEFAULT NULL AFTER HPCoolCOP;
ALTER TABLE dbheatpump CHANGE COLUMN HPAbsEffects HPSourceSink VARCHAR(45) DEFAULT NULL;
ALTER TABLE dbheatpump DROP HPYearManufact;
ALTER TABLE dbheatpump DROP HPUnitsFuelConsum;
ALTER TABLE dbheatpump DROP HPManData;

-- update dbchp
ALTER TABLE dbchp ADD COLUMN Manufacturer VARCHAR(45) DEFAULT NULL;
ALTER TABLE dbchp ADD COLUMN Type VARCHAR(45) DEFAULT NULL AFTER CHPequip;
ALTER TABLE dbchp ADD COLUMN SubType VARCHAR(45) DEFAULT NULL AFTER Type;
ALTER TABLE dbchp ADD COLUMN Reference VARCHAR(200) DEFAULT NULL AFTER SubType;
ALTER TABLE dbchp ADD COLUMN FuelType VARCHAR(45) DEFAULT NULL AFTER CHPPt;
ALTER TABLE dbchp ADD COLUMN FluidSupply INT DEFAULT NULL AFTER Eta_e;
ALTER TABLE dbchp ADD COLUMN Tsupply DOUBLE DEFAULT NULL AFTER FluidSupply;
ALTER TABLE dbchp ADD COLUMN FlowRateSupply DOUBLE DEFAULT NULL AFTER Tsupply;
ALTER TABLE dbchp ADD COLUMN FluidSupply2 INT DEFAULT NULL AFTER FlowRateSupply;
ALTER TABLE dbchp ADD COLUMN Tsupply2 DOUBLE DEFAULT NULL AFTER FluidSupply2;
ALTER TABLE dbchp ADD COLUMN FlowRateSupply2 DOUBLE DEFAULT NULL AFTER Tsupply2;
ALTER TABLE dbchp ADD COLUMN Price DOUBLE DEFAULT NULL AFTER FlowRateSupply2;
ALTER TABLE dbchp ADD COLUMN YearUpdate INT(11) DEFAULT NULL AFTER OMRateVar;

-- update dbboiler
ALTER TABLE dbboiler ADD COLUMN Reference VARCHAR(200) DEFAULT NULL AFTER BoilerType;
ALTER TABLE dbboiler ADD COLUMN FuelConsum DOUBLE DEFAULT NULL AFTER BBEfficiency;
ALTER TABLE dbboiler ADD COLUMN FuelType VARCHAR(45) DEFAULT NULL AFTER FuelConsum;
ALTER TABLE dbboiler ADD COLUMN ElConsum DOUBLE DEFAULT NULL AFTER FuelType;
ALTER TABLE dbboiler ADD COLUMN ExcessAirRatio DOUBLE DEFAULT NULL AFTER Preheater;
ALTER TABLE dbboiler ADD COLUMN YearUpdate INT(11) DEFAULT NULL AFTER BoilerOandMvar;

-- update dbfuel
ALTER TABLE dbfuel CHANGE COLUMN FuelCode FuelType VARCHAR(20) DEFAULT NULL AFTER DBFuelUnit;

-- update dbfluid
ALTER TABLE dbfluid ADD COLUMN FluidDataSource VARCHAR(200) DEFAULT NULL AFTER RefrigerantCode;
ALTER TABLE dbfluid ADD COLUMN FluidCpG DOUBLE DEFAULT NULL AFTER TCond;

-- update dbelectricitymix
ALTER TABLE dbelectricitymix ADD COLUMN PercCHP DOUBLE DEFAULT NULL AFTER PercNukes;

-- update dbbenchmark
ALTER TABLE dbbenchmark CHANGE COLUMN ProductionUnit ProductUnit VARCHAR(45) DEFAULT NULL AFTER Product;
