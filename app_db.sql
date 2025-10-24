CREATE DATABASE IF NOT EXISTS app_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE app_db;

CREATE DATABASE IF NOT EXISTS app_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE app_db;

-- Tabelas de referência (sem chaves estrangeiras)
CREATE TABLE IF NOT EXISTS `categoria` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`nome` VARCHAR(100) NOT NULL,
	PRIMARY KEY(`id`)
);

CREATE TABLE IF NOT EXISTS `fornecedor` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`nome` VARCHAR(100) NOT NULL,
	`telefone` VARCHAR(18) NOT NULL,
	`email` VARCHAR(100) NOT NULL,
	`endereco` VARCHAR(120) NOT NULL,
	PRIMARY KEY(`id`)
);

CREATE TABLE IF NOT EXISTS `cliente` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`nome` VARCHAR(100) NOT NULL,
	`cpf` VARCHAR(16) NULL, -- Corrigido: Permitindo nulo (para clientes PJ)
	`cnpj` VARCHAR(16) NULL, -- Corrigido: Permitindo nulo (para clientes PF)
	`email` VARCHAR(100) NOT NULL,
	`endereco` VARCHAR(200) NOT NULL,
	PRIMARY KEY(`id`)
);

-- Tabela 'item' com as correções
CREATE TABLE IF NOT EXISTS `item` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`nome` VARCHAR(100) NOT NULL,
	`descricao` VARCHAR(300) NULL, -- Corrigido: Permitindo nulo (como no modelo)
	`preco` DECIMAL(10, 2) NOT NULL,
	`tipo` ENUM('PRODUTO', 'SERVICO') NOT NULL,
	`estoque` INTEGER NULL, -- Corrigido: Permitindo nulo (para serviços)
	`imagem_url` VARCHAR(100) NULL, -- ADICIONADO: Coluna que faltava
	`categoria_id` INTEGER NOT NULL,
	`fornecedor_id` INTEGER NOT NULL,
	PRIMARY KEY(`id`),
    -- Chaves estrangeiras definidas aqui para organização
    FOREIGN KEY(`categoria_id`) REFERENCES `categoria`(`id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY(`fornecedor_id`) REFERENCES `fornecedor`(`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Tabelas de transação
CREATE TABLE IF NOT EXISTS `pedido` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`cliente_id` INTEGER NOT NULL,
	`preco_total` DECIMAL(10, 2) NOT NULL,
	`status` ENUM('CANCELADO', 'PENDENTE', 'ENTREGUE') NOT NULL,
	PRIMARY KEY(`id`),
    FOREIGN KEY(`cliente_id`) REFERENCES `cliente`(`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS `item_pedido` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`pedido_id` INTEGER NOT NULL,
	`item_id` INTEGER NOT NULL,
	`quantidade` INTEGER NOT NULL,
	PRIMARY KEY(`id`),
    FOREIGN KEY(`pedido_id`) REFERENCES `pedido`(`id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY(`item_id`) REFERENCES `item`(`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS `atendimento` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`data_atendimento` DATE NOT NULL,
	`item_pedido_id` INTEGER NOT NULL,
	PRIMARY KEY(`id`),
    -- ADICIONADO: Chave estrangeira que faltava
    FOREIGN KEY(`item_pedido_id`) REFERENCES `item_pedido`(`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);


-- INSERINDO DADOS DE EXEMPLO (com correções)

INSERT INTO categoria (nome)
VALUES ('Eletrônicos'), ('Serviços');

INSERT INTO fornecedor (nome, telefone, email, endereco)
VALUES
('Tech Supply Ltda', '(11) 99999-9999', 'contato@techsupply.com', 'Av. Paulista, 1000 - São Paulo'),
('Serviços Pro Ltda', '(21) 98888-8888', 'contato@servicospro.com', 'Rua das Laranjeiras, 50 - Rio de Janeiro');

-- Corrigido: Adicionando 'imagem_url' (como NULL) na lista de colunas
INSERT INTO item (nome, descricao, preco, tipo, estoque, imagem_url, categoria_id, fornecedor_id)
VALUES
('Notebook Lenovo IdeaPad 3', 'Notebook com processador Ryzen 5, 8GB RAM, SSD 256GB', 3499.90, 'PRODUTO', 10, NULL, 1, 1),
('Instalação de Software', 'Serviço de instalação e configuração de software no equipamento', 150.00, 'SERVICO', NULL, NULL, 2, 2);

INSERT INTO cliente (nome, cpf, cnpj, email, endereco)
VALUES ('João da Silva', '123.456.789-00', NULL, 'joao.silva@email.com', 'Rua das Flores, 45 - Rio de Janeiro');

INSERT INTO pedido (cliente_id, preco_total, status)
VALUES
(1, 3499.90, 'PENDENTE'),
(1, 150.00, 'ENTREGUE');

INSERT INTO item_pedido (pedido_id, item_id, quantidade)
VALUES
(1, 1, 1),
(2, 2, 1);

-- Corrigido: Finalizando o INSERT com ponto e vírgula
INSERT INTO atendimento (data_atendimento, item_pedido_id)
VALUES
(CURDATE(), 1);