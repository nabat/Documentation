CREATE TABLE IF NOT EXISTS `documentation` (
  `id` INT(11) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  `wiki` VARCHAR(255) NOT NULL,
  `confluence` VARCHAR(255) NOT NULL
)
  DEFAULT CHARSET = utf8;
  COMMENT = 'Wiki to confluence url'