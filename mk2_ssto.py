#! /usr/bin/env python
import math


g = 9.81

THRUST_NERV_VAC = 60
ISP_NERV_VAC = 800

MASS_NERV = 3

THRUST_RAPIER_JET_M0 = 105
THRUST_RAPIER_JET_M375 = 465.64
ISP_RAPIER_JET = 3200
ISP_RAPIER_ROCKET_ATM = 275
ISP_RAPIER_ROCKET_VAC = 305
ISP_RAPIER_ROCKET_AVG = 290

MASS_RAPIER = 2

LFO_RATIO = 90/110


def cal_fuel_mass(dry_mass: float, isp: float, target_dv: float) -> float:
    mass_ratio = math.e ** (target_dv / isp / g)
    total_mass = dry_mass * mass_ratio
    return total_mass - dry_mass


def cal_dry_mass(init_mass: float, isp: float, target_dv: float) -> float:
    mass_ratio = math.e ** (target_dv / isp / g)
    return init_mass / mass_ratio


def do_some_math(n_nervs: int, n_rapiers: int, lko_twr: float, lko_dv: float):
    lko_total_mass = n_nervs * THRUST_NERV_VAC / lko_twr / g
    lko_dry_mass = cal_dry_mass(lko_total_mass, ISP_NERV_VAC, lko_dv)
    lko_lf_mass = lko_total_mass - lko_dry_mass
    print("LKO:")
    print("total mass:", lko_total_mass)
    print("dry mass:", lko_dry_mass)
    print("LF mass:", lko_lf_mass)

    rocket_dry_mass = lko_total_mass
    rocket_dv = 700
    rocket_isp = ISP_RAPIER_ROCKET_AVG
    rocket_lfo_mass = cal_fuel_mass(rocket_dry_mass, rocket_isp, rocket_dv)
    rocket_total_mass = rocket_dry_mass + rocket_lfo_mass
    print("Rocket:")
    print("total mass:", rocket_total_mass)
    print("LFO mass:", rocket_lfo_mass)

    jet_dry_mass = rocket_total_mass
    jet_dv = 1600 * 1.3
    jet_isp = ISP_RAPIER_JET
    jet_lf_mass = cal_fuel_mass(jet_dry_mass, jet_isp, jet_dv)
    jet_total_mass = jet_dry_mass + jet_lf_mass
    print("Jet:")
    print("total mass:", jet_total_mass)
    print("LF mass:", jet_lf_mass)

    total_lf_mass = lko_lf_mass + jet_lf_mass + \
        rocket_lfo_mass * LFO_RATIO / (1 + LFO_RATIO)
    total_ox_mass = rocket_lfo_mass / (1 + LFO_RATIO)

    total_fuel_mass = total_lf_mass + total_ox_mass
    fuselage_mass = total_fuel_mass / 8

    engines_mass = n_nervs * MASS_NERV + n_rapiers * MASS_RAPIER

    payload_mass = jet_dry_mass - fuselage_mass - \
        engines_mass - total_fuel_mass

    print()
    print("Summary")
    print("Total mass:", jet_total_mass)
    print("Engines mass:", engines_mass)
    print("Fuselage mass:", fuselage_mass)
    print("Payload mass:", payload_mass)
    print("LF mass:", total_lf_mass, ', Unit:', int(total_lf_mass*200))
    print("Ox mass", total_ox_mass, ', Unit:', int(total_ox_mass*200))
    print("Init TWR:", n_rapiers * THRUST_RAPIER_JET_M0 / g / jet_total_mass)


def main():
    do_some_math(2, 2, 0.35, 4000)


if __name__ == '__main__':
    main()
