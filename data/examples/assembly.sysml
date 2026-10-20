// Original documentation example. Source-reviewed; not parser-validated.
package AssemblyExample {
    port def Mount;

    part def Wheel {
        port hub : Mount;
    }

    part def Axle {
        port mount : Mount;
    }

    part def Assembly {
        part wheel : Wheel;
        part axle : Axle;
        ref part spare : Wheel[0..1];
        connection link connect axle.mount to wheel.hub;
    }

    part assembly : Assembly;
}
