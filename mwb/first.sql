-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema trabalho_faculdade
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema trabalho_faculdade
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `trabalho_faculdade` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `trabalho_faculdade` ;

-- -----------------------------------------------------
-- Table `trabalho_faculdade`.`tbl_estoque`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trabalho_faculdade`.`tbl_estoque` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome_produto` VARCHAR(250) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `trabalho_faculdade`.`tbl_produtos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trabalho_faculdade`.`tbl_produtos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome_produto` VARCHAR(100) NOT NULL,
  `desc_produto` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `trabalho_faculdade`.`tbl_material`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trabalho_faculdade`.`tbl_material` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome_material` VARCHAR(100) NOT NULL,
  `unidade_material` VARCHAR(20) NOT NULL,
  `quantidade_estoque` DECIMAL(10,2) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `trabalho_faculdade`.`tbl_formula`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trabalho_faculdade`.`tbl_formula` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `produto_id` INT NULL DEFAULT NULL,
  `materia_prima_id` INT NULL DEFAULT NULL,
  `qtd_necessaria` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `produto_id` (`produto_id` ASC) VISIBLE,
  INDEX `materia_prima_id` (`materia_prima_id` ASC) VISIBLE,
  CONSTRAINT `tbl_formula_ibfk_1`
    FOREIGN KEY (`produto_id`)
    REFERENCES `trabalho_faculdade`.`tbl_produtos` (`id`),
  CONSTRAINT `tbl_formula_ibfk_2`
    FOREIGN KEY (`materia_prima_id`)
    REFERENCES `trabalho_faculdade`.`tbl_material` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
