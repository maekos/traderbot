# traderbot

El bot por ahora lo unico que hace es una consulta a yahoo finance del ticker de AAPL
cada un segundo.

## Requerimientos
- Uso en sistemas LINUX
- Deberán tener docker instalado para ejecutar el robot.

## Uso

Para descargar el entorno de desarrollo ejecutar:

```
make build
```

Para el modo interactivo:

```
make shell
```

Para ejecutar el robot:
```
make run
```
Salida de pantalla:

```
2020-10-02 00:33:24,514 - trader - DEBUG - Broker initialization
[*********************100%***********************]  1 of 1 completed
2020-10-02 00:33:25,170 - trader - INFO - <AAPL> date <2020-01-02T00:00:00.000000000> open: 74.05999755859375, close 75.0875015258789, high 75.1500015258789, low 73.79750061035156 volume:135480400.0
2020-10-02 00:33:26,175 - trader - INFO - <AAPL> date <2020-01-03T00:00:00.000000000> open: 74.2874984741211, close 74.35749816894531, high 75.1449966430664, low 74.125 volume:146322800.0
2020-10-02 00:33:27,187 - trader - INFO - <AAPL> date <2020-01-06T00:00:00.000000000> open: 73.44750213623047, close 74.94999694824219, high 74.98999786376953, low 73.1875 volume:118387200.0
2020-10-02 00:33:28,198 - trader - INFO - <AAPL> date <2020-01-07T00:00:00.000000000> open: 74.95999908447266, close 74.59750366210938, high 75.2249984741211, low 74.37000274658203 volume:108872000.0
...
```
