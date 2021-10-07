-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 16, 2021 at 07:37 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `portfolio_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `asset_data`
--

CREATE TABLE `asset_data` (
  `asset_id` varchar(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `closing_price` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `asset_data`
--

INSERT INTO `asset_data` (`asset_id`, `date`, `closing_price`) VALUES
('IRCTC', '2021-09-07', 3008.4),
('NESTLEIND', '2021-09-07', 20223.2),
('INDIAMART', '2021-09-07', 8920.2);

-- --------------------------------------------------------

--
-- Table structure for table `asset_info`
--

CREATE TABLE `asset_info` (
  `asset_id` varchar(11) NOT NULL,
  `asset_name` varchar(100) DEFAULT NULL,
  `asset_type` varchar(100) NOT NULL DEFAULT 'stock'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `asset_info`
--

INSERT INTO `asset_info` (`asset_id`, `asset_name`, `asset_type`) VALUES
('ATGL', 'ATGL', 'stock'),
('DIVISLAB', 'DIVISLAB', 'stock'),
('DIXON', 'DIXON', 'stock'),
('HINDUNILVR', 'HINDUNILVR', 'stock'),
('INDIAMART', 'INDIAMART', 'stock'),
('INFY', 'INFY', 'stock'),
('IRCTC', 'IRCTC', 'stock'),
('NESTLEIND', 'NESTLEIND', 'stock'),
('POLYCAB', 'POLYCAB', 'stock'),
('TATACONSUM', 'TATACONSUM', 'stock'),
('TCS', 'TCS', 'stock'),
('TITAN', 'TITAN', 'stock');

-- --------------------------------------------------------

--
-- Table structure for table `asset_weights`
--

CREATE TABLE `asset_weights` (
  `asset_id` varchar(11) DEFAULT NULL,
  `portfolio_id` varchar(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `amount` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `asset_weights`
--

INSERT INTO `asset_weights` (`asset_id`, `portfolio_id`, `weight`, `amount`) VALUES
('IRCTC', '1', 25, NULL),
('DIVISLAB', '1', 25, NULL),
('INFY', '1', 25, NULL),
('DIXON', '1', 25, NULL),
('TCS', '2', 50, NULL),
('TITAN', '2', 25, NULL),
('ATGL', '2', 25, NULL),
('tcs', '1', 23, 1000),
('tcs', '1', 23, 1000),
('tcs', '2', 23, 1000),
('tcs', '8879f', 20, 200),
('IRCTC', '8879f', 30, 300),
('tcs', 'e527a', 20, 200),
('IRCTC', 'e527a', 30, 300),
('TCS', '9c961', 50, 22222),
('DIVISLAB', '9c961', 50, 22222);

-- --------------------------------------------------------

--
-- Table structure for table `portfolio_info`
--

CREATE TABLE `portfolio_info` (
  `portfolio_id` varchar(100) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `portfolio_name` varchar(100) NOT NULL,
  `portfolio_investment` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `portfolio_info`
--

INSERT INTO `portfolio_info` (`portfolio_id`, `user_id`, `portfolio_name`, `portfolio_investment`) VALUES
('1', 1, 'portfolio 1', 50000),
('1d4f5', 1, 'test', 1000),
('2', 1, 'port 2', 100000),
('333d5', 1, 'test', 1000),
('447f1', 1, 'test', 1000),
('48d8a', 1, 'test', 1000),
('50aef', 1, 'portdata', 4999),
('513ff', 1, 'test', 1000),
('529-8fe1-4255-9f01-d6843dca4608', 1, 'portdata', 4999),
('5e079', 1, 'test', 1000),
('728b5', 1, 'test', 1000),
('754e8', 1, 'test', 1000),
('7eb8a', 1, 'portdata', 4999),
('820cb', 1, 'test', 1000),
('83f39', 1, 'test', 1000),
('8748a', 1, 'portdata', 4999),
('8879f', 1, 'test', 1000),
('9c961', 1, 'port', 44444),
('9d98d', 1, 'test', 1000),
('afc8a', 1, 'test', 1000),
('b9c88', 1, 'test', 1000),
('c252c', 1, 'test', 1000),
('e527a', 1, 'test', 1000),
('e77bf', 1, 'test', 1000),
('f8e21', 1, 'port', 44444),
('fb36a', 1, 'portdata', 4999),
('test', 1, 'test', 5000);

-- --------------------------------------------------------

--
-- Table structure for table `portfolio_performance`
--

CREATE TABLE `portfolio_performance` (
  `portfolio_id` varchar(11) DEFAULT NULL,
  `five_year_return` float DEFAULT NULL,
  `sharpe_ratio` float DEFAULT NULL,
  `value_at_risk` float DEFAULT NULL,
  `portfolio_beta` float DEFAULT NULL,
  `treynor_ratio` float DEFAULT NULL,
  `jensens_alpha` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `portfolio_performance`
--

INSERT INTO `portfolio_performance` (`portfolio_id`, `five_year_return`, `sharpe_ratio`, `value_at_risk`, `portfolio_beta`, `treynor_ratio`, `jensens_alpha`) VALUES
('1', 120, 2.23, 0.9888, 1.5, 0.98, 1.23),
('2', 150, 10, 10, 10, 10, 10);

-- --------------------------------------------------------

--
-- Table structure for table `user_info`
--

CREATE TABLE `user_info` (
  `user_id` int(11) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(10) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `date_registered` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `address` varchar(200) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_info`
--

INSERT INTO `user_info` (`user_id`, `first_name`, `last_name`, `email`, `mobile`, `dob`, `date_registered`, `address`, `gender`, `username`, `password`) VALUES
(1, 'Tanishq', 'Tapiawala', 'tanishqt50@gmail.com', '9920938318', '2001-02-14', '2021-09-07 00:13:08', 'Goregaon(West)', 'M', 'Tanishq111', 'tanishq111');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `asset_data`
--
ALTER TABLE `asset_data`
  ADD KEY `asset_id` (`asset_id`);

--
-- Indexes for table `asset_info`
--
ALTER TABLE `asset_info`
  ADD PRIMARY KEY (`asset_id`);

--
-- Indexes for table `asset_weights`
--
ALTER TABLE `asset_weights`
  ADD KEY `asset_weights_ibfk_1` (`asset_id`),
  ADD KEY `asset_weights_ibfk_2` (`portfolio_id`);

--
-- Indexes for table `portfolio_info`
--
ALTER TABLE `portfolio_info`
  ADD PRIMARY KEY (`portfolio_id`),
  ADD KEY `portfolio_info_ibfk_1` (`user_id`);

--
-- Indexes for table `portfolio_performance`
--
ALTER TABLE `portfolio_performance`
  ADD UNIQUE KEY `portfolio_id` (`portfolio_id`);

--
-- Indexes for table `user_info`
--
ALTER TABLE `user_info`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `asset_data`
--
ALTER TABLE `asset_data`
  ADD CONSTRAINT `asset_id` FOREIGN KEY (`asset_id`) REFERENCES `asset_info` (`asset_id`);

--
-- Constraints for table `asset_weights`
--
ALTER TABLE `asset_weights`
  ADD CONSTRAINT `asset_weights_ibfk_1` FOREIGN KEY (`asset_id`) REFERENCES `asset_info` (`asset_id`),
  ADD CONSTRAINT `asset_weights_ibfk_2` FOREIGN KEY (`portfolio_id`) REFERENCES `portfolio_info` (`portfolio_id`);

--
-- Constraints for table `portfolio_info`
--
ALTER TABLE `portfolio_info`
  ADD CONSTRAINT `portfolio_info_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`user_id`);

--
-- Constraints for table `portfolio_performance`
--
ALTER TABLE `portfolio_performance`
  ADD CONSTRAINT `ref_id` FOREIGN KEY (`portfolio_id`) REFERENCES `portfolio_info` (`portfolio_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
