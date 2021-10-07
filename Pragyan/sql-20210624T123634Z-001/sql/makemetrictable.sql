CREATE TABLE `MetricsDF` (
	`Portfolio` VARCHAR(11) NOT NULL, 
	`Return` DECIMAL(38, 9) NOT NULL, 
	`Volatility` DECIMAL(38, 9) NOT NULL, 
	`Sharpe Ratio` DECIMAL(38, 9) NOT NULL, 
	`VaR` DECIMAL(38, 9) NOT NULL, 
	`Portfolio Beta` DECIMAL(38, 9) NOT NULL, 
	`Treynor Ratio` DECIMAL(38, 9) NOT NULL, 
	`Jensen Alpha` DECIMAL(38, 9) NOT NULL
);
