# Fog Management:

This function allows the system's administrator manage what application or
even or data analysis it's necessary to improve accuracy or to improve quality
of datas. There is two folders inside folder flushing. manager_fog and
manage_fog_user, the first one is about the crips will be run on fog. The last
one is about the scripts which administrator must run.

The main idea is the administrator of network can transfer scripts to the flushing nodes. The transferency of data use scp protocol to do it. The flushing nodes receives this files, then implements this new function to analyze the data from sensing nodes. The main advantage of use a fog manager that the administrator can change this function any time, so a fogmanagement makes the system more flexible. At the momento, there is two function ready. The first one implements meia of average measurements. This function receives the data from sensing nodes, average the measurmentes the sends to the cloud. The second function delete impossible measures. 



## Detalhes do Funcionamento:
O administrator executa o script adm.py. Este script recebe o nome o modulo
a ser enviado para a fog. Modifica o nome para um nome padrao, envia por scp
e retorna ao nome original do arquivo. Nesta pasta manager_fog_user o admin
tem acesso a todos os modulos disponiveis e pode adicionar outros mais. 
Apos o envio do arquivo. este arquivo e importado e executado pelo fog.
Dessa maneira, o admin pode escolher e trocar os modulos e as analise de dados
a ser executada pela fog.


