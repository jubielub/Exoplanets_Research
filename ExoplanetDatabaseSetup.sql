DROP TABLE IF EXISTS STELLAR_PROPERTIES CASCADE;
DROP TABLE IF EXISTS EXOPLANET_PHYSICAL_PROPERTIES CASCADE;
DROP TABLE IF EXISTS EXOPLANET_STAR CASCADE;
DROP TABLE IF EXISTS PLANET_NA_K_ATMOSPHERIC_ABSORPTION_PAPER_INFO CASCADE;
DROP TABLE IF EXISTS PLANET_NA_K_ATMOSPHERIC_ABSORPTION_CONCLUSION CASCADE;

CREATE TABLE STELLAR_PROPERTIES (
  Star_Name VARCHAR(30) NOT NULL,
  Stellar_Effective_Temperature INTEGER,
  Stellar_Radius FLOAT(5),
  Stellar_Mass FLOAT(5), 
  Stellar_Type VARCHAR(10), 
  Stellar_Surface_Gravity FLOAT(15),
  Stellar_Metallicity FLOAT(15),
  PRIMARY KEY (Star_Name)
);

CREATE TABLE EXOPLANET_PHYSICAL_PROPERTIES (
  Planet_Name VARCHAR(20) NOT NULL, 
  Planet_Mass FLOAT(5),
  Planet_Radius FLOAT(5),
  Period FLOAT(3),
  Orbital_Eccentricity  FLOAT(5),
  Periastron_Argument FLOAT(3),
  Percentage_Of_The_Orbital_Phase_Spent_Within_The_Conservative_Habitable_Zone FLOAT(3),
  Percentage_Of_The_Orbital_Phase_Spent_Within_The_Optimistic_Habitable_Zone FLOAT(3),
  Planetary_Equilibrium_Temperature_Periastron_Hot_Dayside INTEGER,
  Planetary_Equilibrium_Temperature_Periastron_Well_Mixed INTEGER,
  Planetary_Equilibrium_Temperature_Apastron_Hot_Dayside INTEGER,
  Planetary_Equilibrium_Temperature_Apastron_Well_Mixed INTEGER,
  PLanetary_Density FLOAT(5),
  PRIMARY KEY (Planet_Name)
);

CREATE TABLE EXOPLANET_STAR (
  Star_Name VARCHAR(30) NOT NULL,
  Planet_Name VARCHAR(20) NOT NULL,
  PRIMARY KEY(Star_Name, Planet_Name), 
  FOREIGN KEY (Star_Name) REFERENCES STELLAR_PROPERTIES ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (Planet_Name) REFERENCES EXOPLANET_PHYSICAL_PROPERTIES ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE PLANET_NA_K_ATMOSPHERIC_ABSORPTION_PAPER_INFO (
  Planet_Name VARCHAR(20) NOT NULL,
  Paper_Name VARCHAR(70) NOT NULL, 
  Paper_Publication_Date DATE NOT NULL,
  Na_Absorption_Concluded_In_The_Planets_Atmosphere VARCHAR(20) NOT NULL 
  CHECK(Na_Absorption_Concluded_In_The_Planets_Atmosphere = 'Definite Absorption' OR  Na_Absorption_Concluded_In_The_Planets_Atmosphere = 'Potential Absorption' OR Na_Absorption_Concluded_In_The_Planets_Atmosphere = 'No Absorption' OR Na_Absorption_Concluded_In_The_Planets_Atmosphere = 'Not Mentioned'), 
  K_Absorption_Concluded_In_The_Planets_Atmosphere VARCHAR(20) NOT NULL
  CHECK(K_Absorption_Concluded_In_The_Planets_Atmosphere = 'Definite Absorption' OR K_Absorption_Concluded_In_The_Planets_Atmosphere = 'Potential Absorption' OR K_Absorption_Concluded_In_The_Planets_Atmosphere = 'No Absorption' OR K_Absorption_Concluded_In_The_Planets_Atmosphere = 'Not Mentioned'),
  Na_Sigma FLOAT(5),
  K_Sigma FLOAT(5),
  Notes VARCHAR(100),
  Not_High_Enough_Resolution_For_Conclusion BOOLEAN NOT NULL,
  Provides_Bins_Larger_Than_350A BOOLEAN NOT NULL,
  Atmospheric_Effects BOOLEAN NOT NULL,
  PRIMARY KEY(Planet_Name, Paper_Name),
  FOREIGN KEY (Planet_Name) REFERENCES EXOPLANET_PHYSICAL_PROPERTIES
);

CREATE TABLE PLANET_NA_K_ATMOSPHERIC_ABSORPTION_CONCLUSION (
  Planet_Name VARCHAR(20) NOT NULL,
  Na_Absorption_Type VARCHAR(20) NOT NULL
  CHECK(Na_Absorption_Type = 'Definite Absorption' OR Na_Absorption_Type = 'Potential Absorption' OR Na_Absorption_Type = 'No Absorption' OR Na_Absorption_Type = 'Not Enough Information'),
  Reason_For_Concluded_Na_Absorption_Type VARCHAR(70), 
  Reason_For_Concluded_K_Absorption_Type VARCHAR(70),
  PRIMARY KEY(Planet_Name),
  FOREIGN KEY(Planet_Name) REFERENCES EXOPLANET_PHYSICAL_PROPERTIES
);
