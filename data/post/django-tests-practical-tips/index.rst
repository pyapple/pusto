Django tests. Практические советы
=================================
..
    - введение
    - избегайте static fixtures
    - транзакции - наше все
    - в несколько процессов (djtest-bootstrap)
    - трюк с settings
    - cache and redis

С апреля уже не работаю в ostrovok.ru, но опыт по внедрению тестов в разработку, 
полученный в этой команде, очень хороший. Хочу записать по горячим следам ряд практических 
советов и замечаний по поводу внедрения тестов и django тестов в частности.

.. MORE

Внедрять тесты в уже существующий проект с кучей всесторонних зависимостей от внешних 
сервисов и API - задача, требующая довольно много времени. Плюс возвращаться и 
дорабатывать их нужно будет не один раз. Хорошо что в ostrovok.ru все понимали, что тесты 
нужны, просто не знали с какой стороны к ним подойти и нужен был человек, который 
"заражен" тестами и возьмется за внедрение.

Про первые шаги `писал на хабре (26.06.2013)`__, потом позже рассказывал на `Pycon Russia 
(24.02.2013)`__ про оптимизацию и запуск тестов в несколько процессов. Когда уходил из 
ostrovok.ru тестов было ~1000 (6 мин на моем ноутбуке, 4 процесса), через полгода сказали, 
что уже ~1500 (6 мин на CI__ сервере, больше 10 процессов). Тесты удались, хотя 
некоторые места хотелось бы сделать лучше.

__ habr/
__ /s/2013-ru-pycon/
__ http://ru.wikipedia.org/wiki/Непрерывная_интеграция

Поговорим о некоторых проблемах и способах их не допустить.

Транзакции для изоляции базы
----------------------------
В моем мозгу изоляция окружения для конкретного теста - это обязательное условие для 
существования хороших тестов. Для изоляции базы самый верный способ - это транзакции, они 
быстрые. В  начале теста мы открываем транзакцию, а после прохождения теста делаем ее 
откат (rollback), ну и условие напрашивается само - не должно быть прерывания открытой 
транзакции. У нас вышло так, что в процессе бронирования было ручное управление 
транзакциями (это и есть прерывание), а тестов вокруг бронирования у нас было очень много 
(больше всего хотелось покрыть тестами именно этот процесс), поэтому мне пришлось 
придумывать свой механизм изоляции базы на основе ее копирования из шаблона. Хотя `этот 
механизм`__ был быстрее `стандартного в django для этого случая`__, но он был медленнее и 
сложнее транзакций. Поэтому когда делался запуск тестов в несколько процессов, пришлось 
приложить больше усилий, чтоб все наши тесты хорошо работали.

__ /s/2013-ru-pycon/#id14
__ https://docs.djangoproject.com/en/dev/topics/testing/overview/#transactiontestcase

**Нужно стараться, чтоб в транзакциях работали максимум тестов.** Транзакции хорошо 
масштабируются на несколько процессов, а те тесты, в которых тестируются
именно транзакции, лучше пускать отдельно в одном процессе уже после основной пачки 
тестов.

Запуск в несколько процессов
----------------------------
Хорошие тесты - это те, которые запускаешь и через какое-то реальное время получаешь 
фитбек прошли или не прошли, для этого вообще-то тесты и вводятся. Если тесты запускаются 
долго, это плохо скажется на процессе тестирования в команде. Для меня реальное время - до 
10 минут, меньше конечно лучше, но больше - это сигнал, что тесты нужно  срочно ускорять. 
В какой-то момент количество тестов выросло до ~800, время 15 минут, всевозможные 
локальные оптимизации кода в тестах произведены, а время еще нужно было сокращать, т.к. 
тестов становилось все больше. Очень хороший скачек в ускорении тестов - это запуск в 
несколько процессов, хотя этот метод добавляет определенную сложность тестовой среде. 
Кроме изоляции базы на уровне процессов, также необходима изоляция всевозможных кешей, 
redis. У нас вышло все еще сложнее. Реализация тестовой среды как-то была совсем не готова 
к нескольким процессам и нужна была значительная переработка, которая в итоге состоялась. 
Мы перенесли всю логику изоляции всего на уровень ``TestCase``, это нам дало возможность 
не только запустить тесты в несколько потоков, но также и опробовать разные пускальщики: 
nose2__, pytest__, но мы так и остались на nose__ первом. С каждым из пускальщиков были 
какие-то проблемы. ``pytest`` был очень медленным на наших тестах при распараллеливании. 
``nose2`` у нас какое-то время поработал на CI, но он зависал при исключениях в 
многопроцессорном режиме. У nose1 хоть и были проблемы с неработающими плагинами в 
multiprocess, но ``xmlunit`` отчет как-то прикрутили для CI, а без других обходились, 
главное что тесты работали значительно быстрее. На одном хакатоне мы опробовали запускать 
наши тесты на крутом серваке (с 24 ядрами, кажется), так у нас ~800 тестов проходили за 
пару минут в 20 процессов. Но самый большой прирост заметен обычно при 2-4 процессах. На 
моем ноутбуке в 4 процесса тесты проходили меньше 6 минут, но у меня реальных было 2 ядра 
и два виртуальных :)

__ http://nose2.readthedocs.org/en/latest/
__ http://pytest.org/latest/
__ http://nose.readthedocs.org/en/latest/

**Хорошо бы, чтобы тестовая среда была готова к запуску в несколько процессов,** благо 
если учесть, что используются транзакции в тестах, то решается это довольно легко, 
`проект-шаблон доступен на github.`__

__ https://github.com/naskoro/djtest-bootstrap

Mocks
-----
Опять же в моем мозгу сидит, что все внешние вызовы должны быть "замоканы" для того чтоб 
тесты были предсказуемые и быстрые. Даже самый быстрый и надежный сторонний сервис может 
дать сбой или ответить каким-то не совсем ожидаемым способом, и тогда тесты упадут. Но 
тесты не должны падать из-за внешних условий, поэтому мы подменяем действительность моками 
и прописываем те ответы, которые мы ожидаем в тестах. Есть еще ряд случаев, в которых без 
моков не обойтись, это могут быть разные моменты со временем, проверка на прошлое или 
будущее, проверка выпадения исключений и т.п. В общем в проекте с тестами скорее всего 
будут моки, у нас их было много.

Хоть мы имеем дело с динамическим языком python и модуль `mock`__ очень помогает нам, но 
моки - это в своем роде магия, и у модуля ``mock`` есть свои нюансы и ограничения, про 
которые не все разработчики знают. Время от времени моки становились проблемой, особенно 
когда их сайд-эффекты сложно было определить и особенно у тех разработчиков, которые мало 
общались с моками. **К ним нужно привыкнуть, с опытом их использовать и чинить становится 
проще.**

__ https://pypi.python.org/pypi/mock

Зависимость тестов от фикстур
-----------------------------
Если над проектом постоянно работают, статические фикстуры - зло. Мы старались 
использовать минимум фикстур, но совсем без них не обойтись. Все эти сторонние сервисы и 
API требуют моков, а моки за собой тянут фикстуры. У нас статических фикстур было немного, 
были даже скрипты, которые могли их обновлять. Но процесс обновления фикстур не был 
встроен в CI, поэтому зависимость тестов от них стала одной из проблем, которую так до 
конца и не решили.

**По-хорошему, фикстуры должны генерироваться динамически и этот процесс нужно встроить в 
CI.** Сторонние сервисы тоже разрабатываются, и придет время, когда нужно будет обновить 
фикстуры до новой версии. А зависимых тестов может оказаться довольно много, когда в 
команде пишут тесты несколько человек и не все знают про возможные проблемы, а тесты 
писать нужно... Динамические фикстуры или постоянное обновление статических фикстур
препятствуют появлению зависимых тестов.

Вообще фикстуры, по моему мнению, одна из самых сложных задач при долгосрочном 
тестировании, т.е. попасться в капкан зависимости от них довольно легко.
 
Следите за своими тестами
-------------------------
Тесты - это как живой организм, который мы приручаем, а потом за ним нужно следить и 
ухаживать, чтоб этот организм помогал нам в решении продуктовых задач. Да, конечно, 
продуктовые задачи важнее, ведь не тесты делают пользователя счастливым, но они - часть 
процесса разработки и помогают разработчикам быть уверенными в каждодневных изменениях, 
которые они вносят для улучшения продукта. Тесты - это долгосрочная перспектива, а с любым 
долговременным делом связано много сложностей и проблем, которые нужно помнить и 
предугадывать, чтоб вовремя принимать корректирующие решения.

Следите за своими тестами и пусть они вам помогают писать хороший код.
