// ============================================================
// JAMESTOWN AUTONOMOUS HUB - Robotic Grip (Garra de Engrenagens)
// Modelagem parametrica para servo 9g (SG90)
// Global Solution FIAP 2026 - PBML
// ============================================================
// Como usar:
//   F5 = preview rapido | F6 = render final
//   Exportar STL: File > Export > Export as STL
//   Mude as variaveis abaixo e a peca recalcula sozinha.
// ============================================================

/* [Engrenagens] */
gear_teeth   = 12;   // numero de dentes por engrenagem
gear_module  = 2.2;  // modulo (tamanho do dente)
gear_thick   = 5;    // espessura da engrenagem
bore_dia     = 4.2;  // furo central (eixo)

/* [Bracos da garra] */
arm_len      = 42;   // comprimento do braco
arm_w        = 7;    // largura do braco
tip_drop     = 16;   // quanto o bico desce na ponta
tip_len      = 12;   // comprimento do bico
open_angle   = 18;   // abertura da garra (0 = fechada)

/* [Placa-base] */
base_w       = 70;   // largura da placa
base_h       = 34;   // profundidade da placa
base_thick   = 4;    // espessura da placa
mount_hole   = 3.2;  // furos de fixacao (parafuso M3)

/* [Servo / encaixe] */
servo_horn_dia = 8;  // diametro do cubo do horn do servo
clearance      = 0.4; // folga de impressao

/* [Qualidade] */
$fn = 64;

// --- Geometria derivada ---
pitch_r     = (gear_module * gear_teeth) / 2;   // raio primitivo
center_dist = pitch_r * 2;                       // distancia entre eixos
gx          = center_dist / 2;                   // deslocamento de cada eixo

// ============================================================
// PERFIL DE ENGRENAGEM (dentes trapezoidais via polygon)
// ============================================================
module gear_2d(teeth, mod) {
    pr   = (mod * teeth) / 2;     // raio primitivo
    rout = pr + mod;              // raio externo (addendum)
    rin  = pr - 1.25 * mod;       // raio interno (dedendum)
    ang  = 360 / teeth;
    union() {
        circle(r = rin + 0.2);
        for (i = [0 : teeth - 1]) {
            rotate(i * ang)
            polygon(points = [
                [rin * cos(-ang*0.30), rin * sin(-ang*0.30)],
                [rout * cos(-ang*0.12), rout * sin(-ang*0.12)],
                [rout * cos( ang*0.12), rout * sin( ang*0.12)],
                [rin * cos( ang*0.30), rin * sin( ang*0.30)]
            ]);
        }
    }
}

module gear(teeth, mod, h) {
    linear_extrude(height = h)
    difference() {
        gear_2d(teeth, mod);
        circle(d = bore_dia);                       // furo do eixo
    }
    // cubo central para reforco do encaixe do horn
    linear_extrude(height = h + 1.5)
        difference() {
            circle(d = servo_horn_dia + 3);
            circle(d = bore_dia);
        }
}

// ============================================================
// BRACO DA GARRA (perfil em L com bico dobrado)
// ============================================================
module arm_2d() {
    // haste que aponta para FRENTE (+Y), saindo da engrenagem
    hull() {
        circle(d = arm_w + 4);                       // base larga (sobre a engrenagem)
        translate([0, arm_len]) circle(d = arm_w);   // segue reto pra frente
    }
    // ponta curva PARA DENTRO (+X) formando o gancho de preensao
    translate([0, arm_len])
        hull() {
            circle(d = arm_w);
            translate([tip_drop, 0]) circle(d = arm_w - 1);
        }
    // dedo final que avanca (preensao do objeto)
    translate([tip_drop, arm_len])
        hull() {
            circle(d = arm_w - 1);
            translate([0, tip_len]) circle(d = arm_w - 2);
        }
}

module arm(h) {
    linear_extrude(height = h)
    difference() {
        arm_2d();
        circle(d = bore_dia);                        // furo de pivo
    }
}

// ============================================================
// PLACA-BASE com furos de fixacao e eixos
// ============================================================
module base_plate() {
    difference() {
        // placa com cantos arredondados
        linear_extrude(height = base_thick)
            offset(r = 4) offset(r = -4)
                square([base_w, base_h], center = true);
        // furos para os dois eixos
        translate([-gx, 0, -1]) cylinder(d = bore_dia + clearance, h = base_thick + 2);
        translate([ gx, 0, -1]) cylinder(d = bore_dia + clearance, h = base_thick + 2);
        // 4 furos de montagem nos cantos
        for (sx = [-1, 1], sy = [-1, 1])
            translate([sx * (base_w/2 - 6), sy * (base_h/2 - 6), -1])
                cylinder(d = mount_hole, h = base_thick + 2);
    }
    // eixos salientes onde as engrenagens giram
    for (x = [-gx, gx])
        translate([x, 0, base_thick])
            cylinder(d = bore_dia - clearance, h = gear_thick + 4);
}

// ============================================================
// MONTAGEM
// ============================================================
module grip_assembly() {
    // placa-base
    color("DimGray") base_plate();

    // engrenagem + braco ESQUERDO (gira +open_angle)
    translate([-gx, 0, base_thick + 0.5])
        rotate([0, 0,  open_angle]) {
            color("Gainsboro") gear(gear_teeth, gear_module, gear_thick);
            translate([0, 0, gear_thick])
                color("SteelBlue") arm(arm_w - 1);
        }

    // engrenagem + braco DIREITO (espelhado, gira -open_angle)
    translate([ gx, 0, base_thick + 0.5])
        rotate([0, 0, -open_angle])
        mirror([1, 0, 0]) {
            color("Gainsboro") gear(gear_teeth, gear_module, gear_thick);
            translate([0, 0, gear_thick])
                color("SteelBlue") arm(arm_w - 1);
        }
}

grip_assembly();
