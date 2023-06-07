# MON3D-RPi

Bem-vindo ao tutorial de instalação e configuração do sistema **MON3D** para controle e monitoramento remoto de impressoras 3D.
Antes de começar o processo, verifique a disponibilidade dos seguintes itens: 
* Computador com conexão internet;
* Cartão microSD de 8GB (mínimo) e dispositivo de leitura compatível;
* Placa Raspberry Pi (RPi) e fonte de alimentação apropriada; 
* Rede Wi-Fi ou cabo ethernet com conexão internet;
* Teclado USB + monitor de vídeo e cabo HDMI (opcional).

Inicialmente, o cartão microSD deve ser configurado como uma mídia de instalação (*[boot image](https://en.wikipedia.org/wiki/Boot_image)*) do sistema operacional Ubuntu Server. Para isso, baixe e instale o [Raspberry Pi Imager](https://www.raspberrypi.com/software/) e siga as instruções descritas em [How to install Ubuntu Server on your Raspberry Pi](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi). Recomenda-se pular o item 5 (*install a desktop*) do tutorial porque o sistema **MON3D** não utiliza interface gráfica.

Finalizada a configuração, o cartão microSD deve ser inserido no slot da Raspberry Pi e a placa energizada com a fonte de alimentação. Com o sistema ligado, conecte-se ao terminal de controle do Ubuntu Server remotamente através de SSH (vide tutorial), ou fisicamente com o teclado USB + monitor de vídeo e cabo HDMI. Será necessário fazer login com o usuário previamente criado no Raspberry Pi Imager.

> **:warning: Atenção:**\
> Espere algum tempo após a primeira inicialização para que o sistema operacional crie os arquivos de usuário. Caso você não tenha configurado um usuário, o Ubuntu Server utiliza como padrão o `user: ubuntu` e `password: ubuntu` no primeiro login, solicitando a criação de uma nova senha no processo.

### Configurando Ambiente RPi:
Antes de começar a configuração do ambiente RPi, verifique a conexão da placa com a internet usando o comando `ping -c 1 google.com`. Caso você não tenha configurado a rede Wi-Fi no Raspberry Pi Imager, conecte um cabo ethernet com conexão internet temporariamente para executar esses primeiros procedimentos. Posteriormente a rede Wi-Fi poderá ser adicionada pelo sistema **MON3D**.

Uma vez conectado ao terminal do Ubuntu Server, execute o seguinte comando para atualizar os arquivos e pacotes do sistema para a última versão disponível. Será solicitado a senha do usuário para prosseguir a atualização, e uma confirmação `[Y/n]` na qual basta pressionar a tecla `Enter` do teclado.
```
sudo apt-get update && sudo apt-get upgrade
```
Feito isso, reinicie o sistema com o comando `reboot` para aplicar as atualizações. 

Agora vamos verificar a ordem de inicialização do dispositivo para garantir um boot prioritário pelo cartão microSD. Aguarde a renicialização e se conecte novamente à placa. Insira o seguinte comando no terminal: 
```
sudo -E rpi-eeprom-config --edit
```
Utilizando o editor nativo do Ubuntu Server, altere a opção `BOOT_ORDER` para `BOOT_ORDER=0xf41`. Pressione `Ctrl+S` para salvar e `Ctrl+X` para sair do editor. Caso o seu arquivo já esteja com essa configuração ou `BOOT_ORDER` vazio, nenhuma alteração precisa ser feita e você pode sair do editor. Para aplicar as alterações, reinicie a placa RPi novamente com o comando `reboot` e volte ao terminal assim que o processo for finalizado.

> ✅ Estamos quase lá, só mais um pouco! 

Agora utilize o seguinte comando para instalar o gerenciador de versões Git:
```
sudo apt-get install git
```

