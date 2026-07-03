"""
Generador de figuritas SVG a partir de la base de datos "Album Virtual".

Los datos de abajo (JUGADORES) fueron extraídos directamente del script SQL
(tablas Jugador + Seleccion), con 192 jugadores y 48 selecciones.

Convenciones:
- El archivo se nombra "{id}.svg" usando el id del jugador (PK de la tabla
  Jugador), así tu vista puede armar la ruta con
  ~/images/jugadores/@jugador.id.svg sin necesitar slugs ni columnas nuevas.
- Como la tabla Jugador no tiene columna de número de camiseta, en el
  círculo grande de la figurita se muestra el id del jugador.
- El color de cada figurita se genera de forma determinística a partir del
  nombre del país (mismo país = mismo color siempre), ya que la tabla
  Seleccion tampoco tiene una columna de color.
"""

import os

# id, nombre, posicion, pais, color (generados desde la BD real)
JUGADORES = [
    (1, 'Guillermo Ochoa', 'Arquero', 'México', '#D64146'),
    (2, 'Santiago Giménez', 'Delantero', 'México', '#D64146'),
    (3, 'Edson Álvarez', 'Mediocampista', 'México', '#D64146'),
    (4, 'César Montes', 'Defensor', 'México', '#D64146'),
    (5, 'Christian Pulisic', 'Delantero', 'Estados Unidos', '#41D653'),
    (6, 'Weston McKennie', 'Mediocampista', 'Estados Unidos', '#41D653'),
    (7, 'Antonee Robinson', 'Defensor', 'Estados Unidos', '#41D653'),
    (8, 'Matt Turner', 'Arquero', 'Estados Unidos', '#41D653'),
    (9, 'Alphonso Davies', 'Defensor', 'Canadá', '#D69B41'),
    (10, 'Jonathan David', 'Delantero', 'Canadá', '#D69B41'),
    (11, 'Tajon Buchanan', 'Mediocampista', 'Canadá', '#D69B41'),
    (12, 'Stephen Eustáquio', 'Mediocampista', 'Canadá', '#D69B41'),
    (13, 'Chris Wood', 'Delantero', 'Nueva Zelanda', '#4166D6'),
    (14, 'Sarpreet Singh', 'Mediocampista', 'Nueva Zelanda', '#4166D6'),
    (15, 'Liberato Cacace', 'Defensor', 'Nueva Zelanda', '#4166D6'),
    (16, 'Oliver Sail', 'Arquero', 'Nueva Zelanda', '#4166D6'),
    (17, 'Vinícius Júnior', 'Delantero', 'Brasil', '#4941D6'),
    (18, 'Rodrygo', 'Delantero', 'Brasil', '#4941D6'),
    (19, 'Bruno Guimarães', 'Mediocampista', 'Brasil', '#4941D6'),
    (20, 'Marquinhos', 'Defensor', 'Brasil', '#4941D6'),
    (21, 'Lamine Yamal', 'Delantero', 'España', '#D6C041'),
    (22, 'Pedri', 'Mediocampista', 'España', '#D6C041'),
    (23, 'Rodri', 'Mediocampista', 'España', '#D6C041'),
    (24, 'Dani Carvajal', 'Defensor', 'España', '#D6C041'),
    (25, 'Son Heung-min', 'Delantero', 'Corea del Sur', '#41D669'),
    (26, 'Kim Min-jae', 'Defensor', 'Corea del Sur', '#41D669'),
    (27, 'Lee Kang-in', 'Mediocampista', 'Corea del Sur', '#41D669'),
    (28, 'Hwang Hee-chan', 'Delantero', 'Corea del Sur', '#41D669'),
    (29, 'Achraf Hakimi', 'Defensor', 'Marruecos', '#A741D6'),
    (30, 'Brahim Díaz', 'Mediocampista', 'Marruecos', '#A741D6'),
    (31, 'Yassine Bounou', 'Arquero', 'Marruecos', '#A741D6'),
    (32, 'Youssef En-Nesyri', 'Delantero', 'Marruecos', '#A741D6'),
    (33, 'Lionel Messi', 'Delantero', 'Argentina', '#41C5D6'),
    (34, 'Emiliano Martínez', 'Arquero', 'Argentina', '#41C5D6'),
    (35, 'Alexis Mac Allister', 'Mediocampista', 'Argentina', '#41C5D6'),
    (36, 'Cristian Romero', 'Defensor', 'Argentina', '#41C5D6'),
    (37, 'Kylian Mbappé', 'Delantero', 'Francia', '#4169D6'),
    (38, 'Antoine Griezmann', 'Delantero', 'Francia', '#4169D6'),
    (39, 'Aurélien Tchouaméni', 'Mediocampista', 'Francia', '#4169D6'),
    (40, 'William Saliba', 'Defensor', 'Francia', '#4169D6'),
    (41, 'Kaoru Mitoma', 'Delantero', 'Japón', '#87D641'),
    (42, 'Takefusa Kubo', 'Mediocampista', 'Japón', '#87D641'),
    (43, 'Wataru Endo', 'Mediocampista', 'Japón', '#87D641'),
    (44, 'Takehiro Tomiyasu', 'Defensor', 'Japón', '#87D641'),
    (45, 'Mohamed Salah', 'Delantero', 'Egipto', '#4B41D6'),
    (46, 'Mostafa Mohamed', 'Delantero', 'Egipto', '#4B41D6'),
    (47, 'Omar Marmoush', 'Delantero', 'Egipto', '#4B41D6'),
    (48, 'Mohamed Elneny', 'Mediocampista', 'Egipto', '#4B41D6'),
    (49, 'Harry Kane', 'Delantero', 'Inglaterra', '#4191D6'),
    (50, 'Jude Bellingham', 'Mediocampista', 'Inglaterra', '#4191D6'),
    (51, 'Bukayo Saka', 'Delantero', 'Inglaterra', '#4191D6'),
    (52, 'Declan Rice', 'Mediocampista', 'Inglaterra', '#4191D6'),
    (53, 'Jamal Musiala', 'Mediocampista', 'Alemania', '#8C41D6'),
    (54, 'Florian Wirtz', 'Mediocampista', 'Alemania', '#8C41D6'),
    (55, 'Antonio Rüdiger', 'Defensor', 'Alemania', '#8C41D6'),
    (56, 'Kai Havertz', 'Delantero', 'Alemania', '#8C41D6'),
    (57, 'Mathew Ryan', 'Arquero', 'Australia', '#D641D4'),
    (58, 'Harry Souttar', 'Defensor', 'Australia', '#D641D4'),
    (59, 'Jackson Irvine', 'Mediocampista', 'Australia', '#D641D4'),
    (60, 'Craig Goodwin', 'Delantero', 'Australia', '#D641D4'),
    (61, 'André Onana', 'Arquero', 'Camerún', '#41D653'),
    (62, 'Bryan Mbeumo', 'Delantero', 'Camerún', '#41D653'),
    (63, 'Vincent Aboubakar', 'Delantero', 'Camerún', '#41D653'),
    (64, 'Frank Anguissa', 'Mediocampista', 'Camerún', '#41D653'),
    (65, 'Kevin De Bruyne', 'Mediocampista', 'Bélgica', '#9B41D6'),
    (66, 'Romelu Lukaku', 'Delantero', 'Bélgica', '#9B41D6'),
    (67, 'Jérémy Doku', 'Delantero', 'Bélgica', '#9B41D6'),
    (68, 'Wout Faes', 'Defensor', 'Bélgica', '#9B41D6'),
    (69, 'Cristiano Ronaldo', 'Delantero', 'Portugal', '#D69D41'),
    (70, 'Bruno Fernandes', 'Mediocampista', 'Portugal', '#D69D41'),
    (71, 'Rúben Dias', 'Defensor', 'Portugal', '#D69D41'),
    (72, 'Bernardo Silva', 'Mediocampista', 'Portugal', '#D69D41'),
    (73, 'Mehdi Taremi', 'Delantero', 'Irán', '#8941D6'),
    (74, 'Sardar Azmoun', 'Delantero', 'Irán', '#8941D6'),
    (75, 'Alireza Jahanbakhsh', 'Mediocampista', 'Irán', '#8941D6'),
    (76, 'Ehsan Hajsafi', 'Defensor', 'Irán', '#8941D6'),
    (77, 'Sadio Mané', 'Delantero', 'Senegal', '#B641D6'),
    (78, 'Kalidou Koulibaly', 'Defensor', 'Senegal', '#B641D6'),
    (79, 'Nicolas Jackson', 'Delantero', 'Senegal', '#B641D6'),
    (80, 'Pape Matar Sarr', 'Mediocampista', 'Senegal', '#B641D6'),
    (81, 'Virgil van Dijk', 'Defensor', 'Países Bajos', '#7841D6'),
    (82, 'Frenkie de Jong', 'Mediocampista', 'Países Bajos', '#7841D6'),
    (83, 'Xavi Simons', 'Mediocampista', 'Países Bajos', '#7841D6'),
    (84, 'Cody Gakpo', 'Delantero', 'Países Bajos', '#7841D6'),
    (85, 'Gianluigi Donnarumma', 'Arquero', 'Italia', '#415AD6'),
    (86, 'Nicolò Barella', 'Mediocampista', 'Italia', '#415AD6'),
    (87, 'Alessandro Bastoni', 'Defensor', 'Italia', '#415AD6'),
    (88, 'Federico Chiesa', 'Delantero', 'Italia', '#415AD6'),
    (89, 'Salem Al-Dawsari', 'Delantero', 'Arabia Saudita', '#D6AA41'),
    (90, 'Firas Al-Buraikan', 'Delantero', 'Arabia Saudita', '#D6AA41'),
    (91, 'Saud Abdulhamid', 'Defensor', 'Arabia Saudita', '#D6AA41'),
    (92, 'Abdulelah Al-Malki', 'Mediocampista', 'Arabia Saudita', '#D6AA41'),
    (93, 'Ellyes Skhiri', 'Mediocampista', 'Túnez', '#41A7D6'),
    (94, 'Youssef Msakni', 'Delantero', 'Túnez', '#41A7D6'),
    (95, 'Montassar Talbi', 'Defensor', 'Túnez', '#41A7D6'),
    (96, 'Aissa Laidouni', 'Mediocampista', 'Túnez', '#41A7D6'),
    (97, 'Luka Modric', 'Mediocampista', 'Croacia', '#D65341'),
    (98, 'Joško Gvardiol', 'Defensor', 'Croacia', '#D65341'),
    (99, 'Mateo Kovacic', 'Mediocampista', 'Croacia', '#D65341'),
    (100, 'Andrej Kramaric', 'Delantero', 'Croacia', '#D65341'),
    (101, 'Federico Valverde', 'Mediocampista', 'Uruguay', '#41D67D'),
    (102, 'Darwin Núñez', 'Delantero', 'Uruguay', '#41D67D'),
    (103, 'Ronald Araújo', 'Defensor', 'Uruguay', '#41D67D'),
    (104, 'Sergio Rochet', 'Arquero', 'Uruguay', '#41D67D'),
    (105, 'Akram Afif', 'Delantero', 'Catar', '#41CCD6'),
    (106, 'Almoez Ali', 'Delantero', 'Catar', '#41CCD6'),
    (107, 'Hassan Al-Haydos', 'Mediocampista', 'Catar', '#41CCD6'),
    (108, 'Lucas Mendes', 'Defensor', 'Catar', '#41CCD6'),
    (109, 'Riyad Mahrez', 'Delantero', 'Argelia', '#4178D6'),
    (110, 'Ismaël Bennacer', 'Mediocampista', 'Argelia', '#4178D6'),
    (111, 'Said Benrahma', 'Delantero', 'Argelia', '#4178D6'),
    (112, 'Aissa Mandi', 'Defensor', 'Argelia', '#4178D6'),
    (113, 'Luis Díaz', 'Delantero', 'Colombia', '#D64184'),
    (114, 'James Rodríguez', 'Mediocampista', 'Colombia', '#D64184'),
    (115, 'Daniel Muñoz', 'Defensor', 'Colombia', '#D64184'),
    (116, 'Camilo Vargas', 'Arquero', 'Colombia', '#D64184'),
    (117, 'Christian Eriksen', 'Mediocampista', 'Dinamarca', '#75D641'),
    (118, 'Rasmus Højlund', 'Delantero', 'Dinamarca', '#75D641'),
    (119, 'Pierre-Emile Højbjerg', 'Mediocampista', 'Dinamarca', '#75D641'),
    (120, 'Joachim Andersen', 'Defensor', 'Dinamarca', '#75D641'),
    (121, 'Aymen Hussein', 'Delantero', 'Irak', '#B641D6'),
    (122, 'Ali Jasim', 'Mediocampista', 'Irak', '#B641D6'),
    (123, 'Zidane Iqbal', 'Mediocampista', 'Irak', '#B641D6'),
    (124, 'Rebin Sulaka', 'Defensor', 'Irak', '#B641D6'),
    (125, 'Percy Tau', 'Delantero', 'Sudáfrica', '#D64184'),
    (126, 'Ronwen Williams', 'Arquero', 'Sudáfrica', '#D64184'),
    (127, 'Teboho Mokoena', 'Mediocampista', 'Sudáfrica', '#D64184'),
    (128, 'Mothobi Mvala', 'Defensor', 'Sudáfrica', '#D64184'),
    (129, 'Piero Hincapié', 'Defensor', 'Ecuador', '#B441D6'),
    (130, 'Moisés Caicedo', 'Mediocampista', 'Ecuador', '#B441D6'),
    (131, 'Enner Valencia', 'Delantero', 'Ecuador', '#B441D6'),
    (132, 'Kendry Páez', 'Mediocampista', 'Ecuador', '#B441D6'),
    (133, 'Granit Xhaka', 'Mediocampista', 'Suiza', '#D65A41'),
    (134, 'Manuel Akanji', 'Defensor', 'Suiza', '#D65A41'),
    (135, 'Yann Sommer', 'Arquero', 'Suiza', '#D65A41'),
    (136, 'Breel Embolo', 'Delantero', 'Suiza', '#D65A41'),
    (137, 'Ali Mabkhout', 'Delantero', 'Emiratos Árabes Unidos', '#D64187'),
    (138, 'Caio Canedo', 'Delantero', 'Emiratos Árabes Unidos', '#D64187'),
    (139, 'Fabio Lima', 'Mediocampista', 'Emiratos Árabes Unidos', '#D64187'),
    (140, 'Khalid Eisa', 'Arquero', 'Emiratos Árabes Unidos', '#D64187'),
    (141, 'Victor Osimhen', 'Delantero', 'Nigeria', '#6641D6'),
    (142, 'Ademola Lookman', 'Delantero', 'Nigeria', '#6641D6'),
    (143, 'Alex Iwobi', 'Mediocampista', 'Nigeria', '#6641D6'),
    (144, 'William Troost-Ekong', 'Defensor', 'Nigeria', '#6641D6'),
    (145, 'Gianluca Lapadula', 'Delantero', 'Perú', '#D67341'),
    (146, 'Luis Advíncula', 'Defensor', 'Perú', '#D67341'),
    (147, 'Renato Tapia', 'Mediocampista', 'Perú', '#D67341'),
    (148, 'Pedro Gallese', 'Arquero', 'Perú', '#D67341'),
    (149, 'David Alaba', 'Defensor', 'Austria', '#D67D41'),
    (150, 'Marcel Sabitzer', 'Mediocampista', 'Austria', '#D67D41'),
    (151, 'Konrad Laimer', 'Mediocampista', 'Austria', '#D67D41'),
    (152, 'Michael Gregoritsch', 'Delantero', 'Austria', '#D67D41'),
    (153, 'Salaah Al-Yahyaei', 'Mediocampista', 'Omán', '#D65A41'),
    (154, 'Muhsen Al-Ghassani', 'Delantero', 'Omán', '#D65A41'),
    (155, 'Harib Al-Saadi', 'Mediocampista', 'Omán', '#D65A41'),
    (156, 'Faiz Al-Rushaidi', 'Arquero', 'Omán', '#D65A41'),
    (157, 'Mohammed Kudus', 'Mediocampista', 'Ghana', '#418ED6'),
    (158, 'Inaki Williams', 'Delantero', 'Ghana', '#418ED6'),
    (159, 'Thomas Partey', 'Mediocampista', 'Ghana', '#418ED6'),
    (160, 'Jordan Ayew', 'Delantero', 'Ghana', '#418ED6'),
    (161, 'Alexis Sánchez', 'Delantero', 'Chile', '#CA41D6'),
    (162, 'Ben Brereton Díaz', 'Delantero', 'Chile', '#CA41D6'),
    (163, 'Erick Pulgar', 'Mediocampista', 'Chile', '#CA41D6'),
    (164, 'Paulo Díaz', 'Defensor', 'Chile', '#CA41D6'),
    (165, 'Mykhailo Mudryk', 'Delantero', 'Ucrania', '#41BDD6'),
    (166, 'Artem Dovbyk', 'Delantero', 'Ucrania', '#41BDD6'),
    (167, 'Oleksandr Zinchenko', 'Defensor', 'Ucrania', '#41BDD6'),
    (168, 'Andriy Lunin', 'Arquero', 'Ucrania', '#41BDD6'),
    (169, 'Eldor Shomurodov', 'Delantero', 'Uzbekistán', '#41BDD6'),
    (170, 'Otabek Shukurov', 'Mediocampista', 'Uzbekistán', '#41BDD6'),
    (171, 'Abdukodir Khusanov', 'Defensor', 'Uzbekistán', '#41BDD6'),
    (172, 'Jaloliddin Masharipov', 'Mediocampista', 'Uzbekistán', '#41BDD6'),
    (173, 'Franck Kessié', 'Mediocampista', 'Costa de Marfil', '#D141D6'),
    (174, 'Sébastien Haller', 'Delantero', 'Costa de Marfil', '#D141D6'),
    (175, 'Simon Adingra', 'Delantero', 'Costa de Marfil', '#D141D6'),
    (176, 'Evan Ndicka', 'Defensor', 'Costa de Marfil', '#D141D6'),
    (177, 'Miguel Almirón', 'Delantero', 'Paraguay', '#D6C541'),
    (178, 'Julio Enciso', 'Delantero', 'Paraguay', '#D6C541'),
    (179, 'Gustavo Gómez', 'Defensor', 'Paraguay', '#D6C541'),
    (180, 'Mathías Villasanti', 'Mediocampista', 'Paraguay', '#D6C541'),
    (181, 'Robert Lewandowski', 'Delantero', 'Polonia', '#D6B941'),
    (182, 'Piotr Zielinski', 'Mediocampista', 'Polonia', '#D6B941'),
    (183, 'Matty Cash', 'Defensor', 'Polonia', '#D6B941'),
    (184, 'Wojciech Szczesny', 'Arquero', 'Polonia', '#D6B941'),
    (185, 'Wu Lei', 'Delantero', 'China', '#D68241'),
    (186, 'Zhang Yuning', 'Delantero', 'China', '#D68241'),
    (187, 'Jiang Guangtai', 'Defensor', 'China', '#D68241'),
    (188, 'Wang Dalei', 'Arquero', 'China', '#D68241'),
    (189, 'Yves Bissouma', 'Mediocampista', 'Mali', '#4E41D6'),
    (190, 'Amadou Haidara', 'Mediocampista', 'Mali', '#4E41D6'),
    (191, 'Hamari Traoré', 'Defensor', 'Mali', '#4E41D6'),
    (192, 'El Bilal Touré', 'Delantero', 'Mali', '#4E41D6'),
]

TEMPLATE = '''<svg width="200" height="280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad-{id}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ffffff;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="200" height="280" fill="url(#grad-{id})" stroke="#333" stroke-width="3" rx="10"/>
  <rect x="10" y="10" width="180" height="200" fill="#ffffff" opacity="0.3" rx="5"/>
  <text x="100" y="110" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#333" text-anchor="middle">{nombre}</text>
  <text x="100" y="160" font-family="Arial, sans-serif" font-size="48" font-weight="bold" fill="#333" text-anchor="middle">{id}</text>
  <rect x="10" y="220" width="180" height="50" fill="#ffffff" opacity="0.8" rx="5"/>
  <text x="100" y="245" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#333" text-anchor="middle">{pais}</text>
  <text x="100" y="262" font-family="Arial, sans-serif" font-size="12" fill="#666" text-anchor="middle">Mundial 2026</text>
</svg>'''

BASE_PATH = "wwwroot/images/jugadores"


def main():
    os.makedirs(BASE_PATH, exist_ok=True)

    for jid, nombre, posicion, pais, color in JUGADORES:
        svg_content = TEMPLATE.format(
            id=jid,
            nombre=nombre.upper(),
            pais=pais.upper(),
            color=color,
        )

        file_path = os.path.join(BASE_PATH, f"{jid}.svg")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        print(f"✓ {jid}.svg  ({nombre} - {pais})")

    print(f"\n✅ {len(JUGADORES)} figuritas generadas exitosamente en '{BASE_PATH}/'")


if __name__ == "__main__":
    main()
