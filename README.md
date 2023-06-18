<h1 align="center">Goods packer</h1>

![статус](https://github.com/hackathon-team-5/goods_packer/actions/workflows/main.yml/badge.svg?event=push)

<table border="0" cellpadding="0" cellspacing="0" align="center">    
    <tr>          
        <td rowspan="2">
            <img src="https://github.com/hackathon-team-5/goods_packer/blob/backend/backend/static/git/big.jpg" width="400">
        </td>
        <td>
            <img src="https://github.com/hackathon-team-5/goods_packer/blob/backend/backend/static/git/topleft.jpg" width="200">
        </td>
        <td>
            <img src="https://github.com/hackathon-team-5/goods_packer/blob/backend/backend/static/git/topright.jpg" width="200">
        </td>
    </tr>
     <tr>
        <td>
            <img src="https://github.com/hackathon-team-5/goods_packer/blob/backend/backend/static/git/bottomleft.jpg" width="200">
        </td>
        <td>
            <img src="https://github.com/hackathon-team-5/goods_packer/blob/backend/backend/static/git/bottomright.jpg" width="200">
        </td>
    </tr>
</table>

<ol>
<li>сведения о команде:</li>
<br>
<ol>
<p>Christina Antonova - Project Manager</p>
    
<p>Alina Surovtseva - Designer</p>
<p>Anastasia Miagkova- Designer</p>

<p>Borokin Andrey - Backend developer</p>
<p>Dmitrii Annsjaw - Backend developer</p>
    
<p>Aleksandr Ivanov - Data Science</p>
<p>Aleksandr Ivanov - Data Science</p>
<p>Anastacia Khisamieva - Data Science</p>
    
<p>Pavel Rudokopov - Frontend developer</p>
<p>Evgeniia Anikeeva - Frontend developer</p>

</ol>
<li>ссылка на Github Pages</li>
<li>инструкция по сборке и запуску</li>
<ol>
<br>
Установите на сервере docker и docker-compose-plugin;
    
Клонируйте репозитарий
    
```
git clone https://github.com/hackathon-team-5/goods_packer.git
```
    
Перейдите в папку `infra/`;

```
cd goods_packer/infra/
```
Создайте файл `.env`. Шаблон для заполнения файла находится в `.env.example`, оставив без изменения `DOCKER_USERNAME=expext`
    
Запустите проект

```
docker compose up -d --build
```

</ol>    
<li>стэк технологий</li>
</ol>
<ol>
<p>backend:<br />
<span style="text-align: justify;">Django, djangorestframework, PostgreSQL, gunicorn</span></p>
</ol>
<ol>
<li>ссылки на сторонние фреймворки, библиотеки, иконки и шрифты если использовались</li>
<li>ключевые точки для media queries</li>
</ol>
