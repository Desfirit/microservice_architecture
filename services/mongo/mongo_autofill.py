import copy

import pymongo
import random

inst1 = {
	"name": "Институт кибербезопасности и цифровых технологий",
	"department": [
		{
			"name": "КБ-1",
			"specs": [
				{"name": "10.03.01"},
				{"name": "10.05.03"}
			],
			"courses": [
				{"name": "основы информационной безопасности"},
				{"name": "программно-аппаратные средства защиты информации"},
				{"name": "криптографические методы защиты информации"},
				{"name": "организационное и правовое обеспечение информационной безопасности"},
				{"name": "документоведение"},
				{"name": "основы управления информационной безопасностью"},
				{"name": "угрозы информационной безопасности автоматизированных систем"},
				{"name": "техническая защита информации"},
				{"name": "сети и системы передачи информации"},
				{"name": "технологии и методы программирования"},
				{"name": "теоретические основы компьютерной безопасности"},
				{"name": "безопасность операционных систем"},
				{"name": "безопасность вычислительных систем"},
				{"name": "безопасность систем баз данных"},
				{"name": "разработка защищенных автоматизированных систем"},
				{"name": "защита информации от вредоносного программного обеспечения"},
				{"name": "технические средства защиты объектов"},
				{"name": "катастрофоустойчивость информационных систем"},
				{"name": "основы формирования каналов воздействия на информационные системы"},
				{"name": "биометрические системы аутентификации"},
				{"name": "стандарты информационной безопасности"},
				{"name": "инновационные методы защиты информации"},
				{"name": "защита информации от вредоносного программного обеспечения"},
				{"name": "организация и технология защиты конфиденциальной информации на предприятиях"},
				{"name": "основы информационной безопасности"},
				{"name": "программно-аппаратные средства обеспечения информационной безопасности"},
				{"name": "криптографические методы защиты информации"},
				{"name": "организационное и правовое обеспечение информационной безопасности"},
				{"name": "управление информационной безопасностью"},
				{"name": "угрозы информационной безопасности автоматизированных систем"},
				{"name": "техническая защита информации"},
				{"name": "сети и системы передачи информации"},
				{"name": "технологии и методы программирования"},
				{"name": "теоретические основы компьютерной безопасности"},
				{"name": "безопасность операционных систем"},
				{"name": "безопасность вычислительных систем"},
				{"name": "безопасность систем баз данных"},
				{"name": "разработка и эксплуатация защищенных автоматизированных систем"},
				{"name": "защита информации от вредоносного программного обеспечения"},
				{"name": "оценка информационной безопасности автоматизированных систем в защищенном исполнении"},
				{"name": "создание автоматизированных систем в защищенном исполнении"},
				{"name": "организация и технология защиты конфиденциальной информации на предприятиях"},
				{"name": "технические средства защиты объектов"},
				{"name": "катастрофоустойчивость информационных систем"},
				{"name": "безопасность сетей ЭВМ"},
				{"name": "физические принципы формирования каналов воздействия на информационные системы"},
				{"name": "организация ЭВМ и вычислительных систем"},
				{"name": "основы теории надежности"},
				{"name": "инфраструктура открытых ключей в системах защиты информации"},
				{"name": "инновационные методы защиты информации"}
			]
		},
		{
			"name": "КБ-2",
			"specs": [
				{"name": "10.05.04"}
			],
			"courses": [
				{"name": "Безопасность информационно-аналитических систем"},
				{"name": "Безопасность операционных систем"},
				{"name": "Языки программирования"},
				{"name": "Технологии и методы программирования"},
				{"name": "Принципы построения, проектирования и эксплуатации информационно-аналитических систем"},
				{"name": "Базы данных и экспертные системы"},
				{"name": "Методы анализа данных"},
				{"name": "Распределенные информационно-аналитические системы"},
				{"name": "Моделирование информационно-аналитических систем"},
				{"name": "Методология и организация информационно-аналитической деятельности"},
				{"name": "Разработка мобильных компонент анализа безопасности информационно-аналитических систем"},
				{"name": "Технологии ситуационных центров"},
				{"name": "Формализованные модели и методы решения аналитических задач"},
				{"name": "Методы анализа естественно-языковых текстов"},
				{"name": "Математические методы в задачах автоматизации информационно-аналитической деятельности"},
				{"name": "Безопасность прикладных информационных технологий и систем"},
				{"name": "Модели управления доступом и информационными потоками в компьютерных системах"},
				{"name": "Технологии организации и хранения информации"},
				{"name": "Технологии информационного взаимодействия компонент информационно-аналитических систем"},
				{"name": "Методы и средства проектирования информационно-аналитических систем"},
				{"name": "Методы и средства передачи информации"},
				{"name": "Техническое обеспечение защиты информации в информационно-аналитических систем"},
				{"name": "Методы обеспечения целостности информации"},
				{"name": "Безопасность автоматизированных систем управления технологическими процессами"},
				{"name": "Методы и алгоритмы аутентификации компонент информационно-аналитических систем"},
				{"name": "Разработка конфигурации и состава обеспечивающей части информационно-аналитической системы"},
				{"name": "Проектирование информационно-аналитических систем в защищенном исполнении"},
				{"name": "Эксплуатация информационно-аналитических систем безопасности"},
				{"name": "Проектирование и разработка безопасного программного обеспечения информационно-аналитических систем"},
				{"name": "Модели и методы оценки качества конфигурации и состава программного обеспечения информационно-аналитических систем"},
				{"name": "Разработка проектов нормативных документов по защите информации"},
				{"name": "Применение технологий искусственного интеллекта и и машинного обучения для поиска угроз информационной безопасности"},
				{"name": "Проектирование и разработка информационно-аналитических систем обеспечения процессов информационной безопасности"},
				{"name": "Информационно-аналитические технологии поиска угроз информационной безопасности"},
				{"name": "Методы и способы расследования инцидентов информационной безопасности"},
				{"name": "Анализ компьютерных инцидентов"}
			]
		},
		{
			"name": "КБ-3",
			"specs": [
				{"name": "09.03.02"}
			],
			"courses": [
				{"name": "Математический анализ"},
				{"name": "Физика"},
				{"name": "Иностранный язык"},
				{"name": "Технологии программирования"},
				{"name": "Линейная алгебра и аналитическая геометрия"},
				{"name": "Разработка программного обеспечения защищенных операционных систем"},
				{"name": "Алгоритмы и структуры данных"},
				{"name": "Методы и средства объектно-ориентированного программирования и проектирования"},
				{"name": "Базы данных и экспертные системы"},
				{"name": "Методы и средства проектирования информационных систем и технологий"},
				{"name": "Теория вероятностей и математическая статистика"},
				{"name": "Анализ сложности алгоритмов"},
				{"name": "Сетевые технологии"},
				{"name": "Веб-программирование"},
				{"name": "Методы и средства разработки компонент программного обеспечения"},
				{"name": "Модели и методы принятия технических решений"},
				{"name": "Моделирование систем"},
				{"name": "Методы искусственного интеллекта"},
				{"name": "Безопасность прикладных информационных технологий и систем"},
				{"name": "Методы и средства взаимодействия компонент программного обеспечения"},
				{"name": "Модели управления доступом и информационными потоками в компьютерных системах"},
				{"name": "Алгоритмы компонентов поточно-параллельной обработки и преобразования данных"},
				{
					"name": "Принципы, технологии и средства организации данных компонентов и программного обеспечения"},
				{"name": "Технологии кроссплатформенного программирования"},
				{"name": "Методы и средства защиты компьютерной информации"},
				{"name": "Разработка мобильных компонент анализа безопасности программного обеспечения"},
				{"name": "Алгоритмы компонентов цифровой обработки данных"},
				{"name": "Компьютерная криминалистика"},
				{"name": "Основы антикоррупционной деятельности"}
			]
		},
		{
			"name": "КБ-4",
			"specs": [
				{"name": "10.05.05"}
			],
			"courses": [
				{"name": "Информационные системы и технологии в правоохранительной сфере"},
				{"name": "Теория информационной безопасности и методология защиты информации"},
				{"name": "Математические основы обработки информации"},
				{"name": "Средства вычислительной техники"},
				{"name": "Кроссплатформенная среда исполнения программного обеспечения"},
				{"name": "Интерпретируемый язык программирования высокого уровня"},
				{"name": "Правовая защита информации"},
				{"name": "Системы и сети передачи информации"},
				{"name": "Теория операционных систем"},
				{"name": "Организация компьютерных сетей"},
				{"name": "Техники реверс-инжиниринга"},
				{"name": "Клиент-серверные системы управления банком данных"},
				{"name": "Теория баз данных Интеллектуальный анализ данных"},
				{"name": "Основы организации и проведения компьютерной экспертизы"},
				{"name": "Технология защищенного документооборота"},
				{"name": "Организационная защита информации"},
				{"name": "Методы и средства защиты информации"},
				{"name": "Системы мониторинга и управления инцидентами информационной безопасности"},
				{"name": "Методы обработки больших объемов данных"},
				{"name": "Моделирование процессов и систем в экспертной деятельности"},
				{"name": "Исследование программного кода"},
				{"name": "Следообразование в операционных системах и базах данных"},
				{"name": "Компьютерная экспертиза"},
				{"name": "Экспертиза веб-приложений"},
				{"name": "Информационно-аналитические системы экспертной деятельности"},
				{"name": "Мониторинг безопасности и обнаружения киберугроз"}
			]
		}
	]
}
inst2 = {
	"name": "Институт информационных технологий",
	"department": [
		{
			"name": "БК-231",
			"specs": [
				{"name": "09.03.04"}
			],
			"courses": [
				{"name": "Теория формальных языков"},
				{"name": "Теория принятия решений"},
				{"name": "Многоагентное моделирование"},
				{"name": "Проектирование программных инструментальных средств для систем поддержки принятия решений"},
				{"name": "Программное обеспечение интеллектуальных систем"},
				{"name": "Проектирование систем поддержки принятия решений"},
				{"name": "Проектирование и обучение нейронных сетей"},
				{"name": "Разработка программных платформ для систем поддержки принятия решений"},
				{"name": "Проектирование экспертных систем"},
				{"name": "Системный анализ предметных областей разработки и внедрения интеллектуальных систем"},
				{"name": "Организация облачных вычислений"},
				{"name": "Технологии обучения интеллектуальных систем"}
			]
		},
		{
			"name": "БК-232",
			"specs": [
				{"name": "09.03.01"}
			],
			"courses": [
				{"name": "Информационно-технологическая инфраструктура"},
				{"name": "Предметно-ориентированные информационные системы"},
				{"name": "Схемотехника устройств компьютерных систем"},
				{"name": "Технологии хранения данных (курс HCIA-Storage)"},
				{"name": "Системы хранения данных (курс HCIP-Storage)"},
				{"name": "Технологии передачи данных (курс HCIA-Datacom)"},
				{"name": "Технологии беспроводных локальных сетей (курс HCIA-WLAN)"},
				{"name": "Технологии облачных сервисов (курс HCIA-Cloud Service)"},
				{"name": "Технологии искусственного интеллекта (курс HCIA-AI)"},
				{"name": "Системы передачи данных (курс HCIP-Datacom)"},
				{"name": "Технологии сетевой безопасности (курс HCIA-Security)"},
				{"name": "Технологии мобильной связи (курс HCIA-5G)"},
				{"name": "Технологии облачных вычислений (курс HCIA-Cloud Computing)"},
				{"name": "Технологии интеллектуальных вычислений (курс HCIA-Intelligent Computing)"},
				{"name": "Теория автоматов"},
				{"name": "Контроль и диагностика цифровых устройств и систем"},
				{"name": "Разработка и программирование микропроцессорных систем"},
				{"name": "Проектирование вычислительных комплексов"},
				{"name": "Эксплуатация сетевой инфраструктуры"},
				{"name": "Проектирование и разработка систем на базе ПЛИС"},
				{"name": "Архитектура процессоров и микропроцессоров"},
				{"name": "Схемотехника устройств компьютерных систем"},
				{"name": "Техническое обслуживание программно-аппаратных комплексов"},
				{"name": "Технология эксплуатации вычислительных комплексов и систем"},
				{"name": "Архитектура вычислительных машин и систем"},
				{"name": "Системное программное обеспечение"},
				{"name": "Интерфейсы и периферийные устройства"}
			]
		},
		{
			"name": "БК-238",
			"specs": [
				{"name": "09.04.01"}
			], 
			"courses": [
				{"name": "Интеллектуальные системы для анализа и синтеза инфокоммуникационных систем"},
				{"name": "Архитектура устройств и систем вычислительной техники"},
				{"name": "Инструментальные средства систем автоматизированного программирования для проектирования систем на кристалле"},
				{"name": "Верификация программных и аппаратных проектов в системах автоматизированного проектирования"},
				{"name": "Технология проектирования устройств и систем"},
				{"name": "Разработка цифровых устройств на базе программируемых логических интегральных схем"},
				{"name": "Методы проектирования цифровых устройств в составе инфокоммуникационных систем"},
				{"name": "Контроль и диагностика цифровых устройств в инфокоммуникационных системах"}
			]
		},
		{
			"name": "БК-239",
			"specs": [
				{
					"name": "09.03.03"
				}
			],
			"courses": [
				{"name": "Предметно-ориентированные информационные системы"},
				{"name": "Архитектура организаций"},
				{"name": "Субъектно-ориентированное моделирование"},
				{"name": "Разработка конфигураций в среде 1С: Предприятие"},
				{"name": "Управление информационно-технологическими сервисами и контентом"},
				{"name": "Методы анализа данных"},
				{"name": "Реинжиниринг бизнес-процессов"},
				{"name": "Проектирование предметно-ориентированных информационных систем"},
				{"name": "Разработка обеспечивающих подсистем"},
				{"name": "Информационный менеджмент"},
				{"name": "Информационно-технологическая инфраструктура"},
				{"name": "Прогнозно-аналитические системы"},
				{"name": "Технологии контроллинга бизнес-процессов"}
			]
		}
	]
}
inst3 = {
	"name": "Институт радиоэлектроники и информатики",
	"department": [
		{
			"name": "БК-332",

			"specs": [
				{"name": "11.03.01"},
				{"name": "11.05.01"}
			],

			"courses": [
				{"name": "Радиоинжиниринг"},
				{"name": "Радиомониторинг и радиоидентификация"},
				{"name": "Телеметрия, сигнальные приборы и датчики радиоэлектронных средств"},
				{"name": "Радиоэлектронные преобразователи и детекторы телеметрических величин"},
				{"name": "Разработка и эксплуатация радиотелеметрических систем"},
				{"name": "Конструкторско-технологическое проектирование радиоэлектронных средств"},
				{"name": "Схемотехника электронных устройств"},
				{"name": "Элементная база радиоэлектроники"},
				{"name": "Модули и техника сверхвысоких частот"},
				{"name": "Электродинамика и распространение радиоволн"},
				{"name": "Сигнальные процессы радиотехнических систем"},
				{"name": "Устройства генерирования и формирования сигналов"},
				{"name": "Устройства приема и преобразования сигналов"},
				{"name": "Цифровая обработка сигналов"},
				{"name": "Численные методы моделирования в радиофизике"},
				{"name": "Цифровые устройства и микропроцессоры"},
				{"name": "Тепловизионная термография"},
				{"name": "Управление качеством в радиоэлектронике"},
				{"name": "Национальная система информационной безопасности"},
				{"name": "Программно-конфигурируемые радиотехнологии"},
				{"name": "Программно-архитектурное проектирование радиотехнических систем"},
				{"name": "Радиоавтоматика"},
				{"name": "Устройства генерирования и формирования сигналов"},
				{"name": "Основы теории радиолокационных систем и комплексов"},
				{"name": "Основы теории радионавигационных систем и комплексов"},
				{"name": "Основы теории радиосистем и комплексов управления"},
				{"name": "Системы космического мониторинга земной поверхности"},
				{"name": "Теория надежности"}
			]
		},
		{
			"name": "БК-335",
			"specs": [
				{"name": "11.03.03"}
			],

			"courses": [
				{"name": "Разработка конструкторской и технологической документации"},
				{"name": "Системы автоматизированного проектирования конструкций радиоэлектронных средств"},
				{"name": "Алгоритмическое обеспечение систем автоматизированного проектирования радиоэлектронных средств"},
				{"name": "Иерархическое проектирование базовых несущих конструкций радиоэлектронных средств"},
				{"name": "Параметрическая идентификация конструкций радиоэлектронных средств"},
				{"name": "Методы и средства контроля технического состояния конструкций радиоэлектронных средств"},
				{"name": "Сквозное автоматизированное проектирования радиоэлектронных средств"},
				{"name": "Технологическая подготовка производства"},
				{"name": "Автоматизированное проектирование модулей сверхвысокочастотного диапазона"}
			]
		},
		{
			"name": "БК-338",
			"specs": [
				{"name": "11.03.02"}
			],
			"courses": [
				{"name": "Цифровые технологии телепроизводства"},
				{"name": "Цифровые радиотрансиверы и медиаконверторы"},
				{"name": "Аудиовизуальные радиосистемы и технологии медиасвязи"},
				{"name": "Кросс-платформенное программирование радиоэлектронных средств"},
				{"name": "Радиоинформационные технологии связи и управления"},
				{"name": "Беспроводные интерфейсы, широкополосные и сверхширокополосные технологии медиадоступа"},
				{"name": "Сигнальные аудиоконсоли и медиасеквенсоры"},
				{"name": "Сигнальная алгоритмистика и радиоавтоматика"},
				{"name": "Разработка и эксплуатация радиотелеметрических систем"},
				{"name": "Программно-конфигурируемые радиотехнологи"},
				{"name": "Схемотехника электронных устройств"},
				{"name": "Цифровые устройства и микропроцессоры"},
				{"name": "Помехоустойчивые методы кодирования и обработки радиосигналов"},
				{"name": "Оптимальные методы пространственного кодирования радиосигналов"},
				{"name": "Цифровая обработка сигналов"},
				{"name": "Модули и техника сверхвысоких частот"},
				{"name": "Коммутация и маршрутизация в сетях связи"}
			]
		},
		{
			"name": "Кафедра геоинформационных систем",
			"specs": [
				{"name": "05.03.03"}
			],

			"courses": [
				{"name": "Основы геоинформационных систем"},
				{"name": "Основы дистанционного зондирования Земли и фотограмметрия"},
				{"name": "Основы трёхмерного моделирования"},
				{"name": "Веб-программирование"},
				{"name": "Математическая картография"},
				{"name": "Базы данных"},
				{"name": "Основы геодезии"},
				{"name": "Геоинформационное картографирование"},
				{"name": "Автоматизированная обработка аэрокосмических снимков"},
				{"name": "Проектирование и использование баз геоданных"},
				{"name": "Геоинформационный анализ"},
				{"name": "Дешифрирование аэрокосмических снимков"},
				{"name": "Создание цифровых моделей рельефа и местности"},
				{"name": "Инфографика в геоинформационных системах"}
			]
		}
	]
}

def create_info_about_course(name):
	return {'name': name, 'fullInfo': 'Полная информация о курсе ' + name}

courses = []

def parse_inst(inst, institutes, department, specs):
	# fill institute
	current_inst = copy.deepcopy(inst)
	#for el in current_inst['department']:
		#del el['specs']
	institutes.insert_one(current_inst)

	# fill department
	for dep in inst['department']:
		current_dep = copy.deepcopy(dep)
		current_dep['prepod_count'] = random.randint(15, 40);
		department.insert_one(current_dep)

		# fill specialization
		for spec in dep['specs']:
			current_spec = copy.deepcopy(spec)
			specs.insert_one(current_spec)

		# fill courses
		for course in dep['courses']:
			if course['name'] not in courses:
				courses.append(course['name'])

def create_scheme(mongo):
	institutes = mongo['institutes']
	department = mongo['department']
	specs = mongo['specializaties']
	courses = mongo['courses']
	parse_inst(inst1, institutes, department, specs, courses)
	parse_inst(inst2, institutes, department, specs, courses)
	parse_inst(inst3, institutes, department, specs, courses)
	#for course in courses:
		#mongo_courses.insert_one(create_info_about_course(course))