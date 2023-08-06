***************************************************************
.gov.br: Pacote de Portlets
***************************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
==========

Este pacote provê a instalação de produto com pacote de portlets multimídia seguindo padrão de estilização do Portal Padrão.

Requisitos
==========

Este pacote foi desenvolvido especificadamente para o Portal Padrão, dessa forma, para uso sem erros de funcionalidades e estilização é indicado que seja utilizado como complemento ao Portal Padrão.


Estado deste pacote
===================

O **brasil.gov.portlets** tem testes automatizados e, a cada alteração em seu
código os testes são executados pelo serviço Travis.

O estado atual dos testes pode ser visto nas imagens a seguir:

.. image:: http://img.shields.io/pypi/v/brasil.gov.portlets.svg
    :target: https://pypi.python.org/pypi/brasil.gov.portlets

.. image:: https://img.shields.io/travis/plonegovbr/brasil.gov.portlets/master.svg
    :target: http://travis-ci.org/plonegovbr/brasil.gov.portlets

.. image:: https://img.shields.io/coveralls/plonegovbr/brasil.gov.portlets/master.svg
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.portlets

Instalação
==========

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``brasil.gov.portlets`` à lista de eggs da instalação::

        [buildout]
        ...
        eggs =
            brasil.gov.portlets

2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Acesse o painel de controle e instale o produto
**brasil.gov.portlets: Instalação do Pacote**.
