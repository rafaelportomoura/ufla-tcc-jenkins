# :newspaper: Jenkis

Este repositório contém o código do microsserviço *Jenkins* do projeto [`CompraVirtual`][compravirtual].  
O microsserviço é responsável pelo continuos deployment e para cumprir essa responsabilidade, o mesmo possui as seguintes funcionalidades:

- Criação da máquina do Jenkins
- Definições de pipelines
- Scripts compartilhados
- Criação do comando de configuração da máquina do jenkins

## :computer: Tecnologias Utilizadas

- [Python][python]: linguagem de programação, foi utilizado para os scripts de deploy

- [Amazon Elastic Compute Cloud (Amazon EC2)][ec2]: oferece a plataforma de computação

- [Jenkins][jenkins]: servidor de automação, fornece centenas de plug-ins para apoiar a construção, implantação e automação do projeto.

- [Jenkins DSL][dsl]: O plugin DSL permite que os trabalhos do Jenkins sejam definidos de forma programática em um arquivo legível por humanos.

- [AWS Systems Manager (SSM)][system-manager]: é uma solução de gerenciamento para recursos na AWS e em ambientes de várias nuvens e híbridos.

- [AWS CodeCommit][codecommit] é um serviço de controle de código-fonte que hospeda repositórios privados do Git.

## :scroll: Autores

 | [<img src="https://github.com/rafaelportomoura.png" width=115><br><sub>Rafael Moura</sub>](https://github.com/rafaelportomoura) <br><sub>Aluno de Graduação</sub>| [<img src="https://github.com/rterrabh.png" width=115><br><sub>Ricardo Terra</sub>](https://github.com/rterrabh) <br><sub>Orientador</sub>|
| :---: | :---: |

## :ticket: Licença

Este repositório é distribuído sob a Licença MIT. Consulte o arquivo [LICENSE](./LICENSE) para obter detalhes.

<!--
LINKS
-->
[compravirtual]: https://github.com/rafaelportomoura/ufla-tcc
[python]: https://www.python.org/
[ec2]: https://aws.amazon.com/pt/ec2
[jenkins]: https://www.jenkins.io/
[system-manager]: https://aws.amazon.com/systems-manager
[dsl]: https://github.com/jenkinsci/job-dsl-plugin
[codecommit]: https://aws.amazon.com/pt/codecommit/