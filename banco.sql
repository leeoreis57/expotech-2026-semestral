CREATE DATABASE IF NOT EXISTS biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE biblioteca;

CREATE TABLE IF NOT EXISTS tbl_usuarios (
    id_usuario      INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario    VARCHAR(100)                  NOT NULL,
    cpf_usuario     VARCHAR(14)                   DEFAULT '',
    telefone_usuario VARCHAR(20)                  DEFAULT '',
    username_usuario VARCHAR(50)                  NOT NULL UNIQUE,
    senha_usuario   VARCHAR(255)                  NOT NULL,
    tipo_usuario    ENUM('admin', 'leitor')       NOT NULL DEFAULT 'leitor'
);

CREATE TABLE IF NOT EXISTS tbl_livros (
    id_livro    INT AUTO_INCREMENT PRIMARY KEY,
    nome_livro  VARCHAR(150) NOT NULL,
    autor_livro VARCHAR(100) NOT NULL,
    ano_livro   YEAR         NOT NULL,
    genero_livro VARCHAR(80) NOT NULL,
    qnt_livro   INT          NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tbl_emprestimos (
    id_emprestimo   INT AUTO_INCREMENT PRIMARY KEY,
    id_livro        INT  NOT NULL,
    id_leitor       INT  NOT NULL,
    data_emprestimo DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_devolucao  DATETIME DEFAULT NULL,
    FOREIGN KEY (id_livro)  REFERENCES tbl_livros(id_livro),
    FOREIGN KEY (id_leitor) REFERENCES tbl_usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS tbl_favoritos (
    id_favorito INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario  INT NOT NULL,
    id_livro    INT NOT NULL,
    UNIQUE KEY uq_favorito (id_usuario, id_livro),
    FOREIGN KEY (id_usuario) REFERENCES tbl_usuarios(id_usuario),
    FOREIGN KEY (id_livro)   REFERENCES tbl_livros(id_livro)
);
 -- Foreign keys de tbl_emprestimos
  ALTER TABLE tbl_emprestimos
  ADD CONSTRAINT fk_livro
  FOREIGN KEY (id_livro)
  REFERENCES tbl_livros(id_livro);

  ALTER TABLE tbl_emprestimos
  ADD CONSTRAINT fk_leitor
  FOREIGN KEY (id_leitor)
  REFERENCES tbl_usuarios(id_usuario);

  -- Foreign keys de tbl_favoritos
  ALTER TABLE tbl_favoritos
  ADD CONSTRAINT fk_favorito_usuario
  FOREIGN KEY (id_usuario)
  REFERENCES tbl_usuarios(id_usuario);

  ALTER TABLE tbl_favoritos
  ADD CONSTRAINT fk_favorito_livro
  FOREIGN KEY (id_livro)
  REFERENCES tbl_livros(id_livro);


  -- Inserts
  INSERT INTO tbl_usuarios
  (nome_usuario, cpf_usuario, telefone_usuario, username_usuario, senha_usuario, tipo_usuario)
  VALUES
('Maria', '12345678900', '11999999999', 'maria', '123', 'leitor'),
('Carlos', '98765432100', '11888888888', 'carlos', '123', 'leitor'),
('Ana', '11122233344', '11777777777', 'ana', '123', 'admin');

INSERT INTO tbl_livros (nome_livro, autor_livro, ano_livro, genero_livro, qnt_livro) VALUES
('Dom Casmurro',                     'Machado de Assis',         1899, 'Romance',         3),
('O Cortiço',                        'Aluísio Azevedo',          1890, 'Naturalismo',     2),
('Vidas Secas',                      'Graciliano Ramos',         1938, 'Romance',         3),
('Grande Sertão: Veredas',           'João Guimarães Rosa',      1956, 'Romance',         2),
('O Senhor dos Anéis',               'J.R.R. Tolkien',           1954, 'Fantasia',        4),
('Harry Potter e a Pedra Filosofal', 'J.K. Rowling',             1997, 'Fantasia',        5),
('1984',                             'George Orwell',            1949, 'Distopia',        3),
('O Pequeno Príncipe',               'Antoine de Saint-Exupéry', 1943, 'Fábula',          4),
('A Culpa é das Estrelas',           'John Green',               2012, 'Romance',         3),
('Sapiens',                          'Yuval Noah Harari',        2011, 'Não-ficção',      2);

INSERT INTO tbl_emprestimos
  (id_livro, id_leitor)
  VALUES
  (1, 1),
  (2, 2);

  INSERT INTO tbl_favoritos
  (id_usuario, id_livro)
  VALUES
  (1, 1),
  (1, 2),
  (2, 4),
  (3, 3);