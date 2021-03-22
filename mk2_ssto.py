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
ISP_RAPIER_ROCKET_AVG = 300

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
    # we need more deltaV to final accelerate and circlarize orbit
    bonus_dv = 300

    lko_total_mass = n_nervs * THRUST_NERV_VAC / lko_twr / g
    lko_dry_mass = cal_dry_mass(lko_total_mass, ISP_NERV_VAC, lko_dv+bonus_dv)
    lko_lf_mass = lko_total_mass - lko_dry_mass
    print("LKO:")
    print(f"Total mass: {lko_total_mass}t")
    print(f"Dry mass: {lko_dry_mass}t")
    print(f"LF mass: {lko_lf_mass}t")
    print()

    rocket_dry_mass = lko_total_mass
    rocket_dv = 700
    rocket_isp = ISP_RAPIER_ROCKET_VAC
    rocket_lfo_mass = cal_fuel_mass(rocket_dry_mass, rocket_isp, rocket_dv)
    rocket_total_mass = rocket_dry_mass + rocket_lfo_mass
    print("Rocket(RAPIERs in closedcycle mode):")
    print(f"Total mass: {rocket_total_mass}t")
    print(f"LFO mass: {rocket_lfo_mass}t")
    print()

    jet_dry_mass = rocket_total_mass
    air_drag_loss = 1200  # empirical value
    gravity_loss = 500    # empirical value
    jet_dv = 1400 + air_drag_loss + gravity_loss
    jet_isp = ISP_RAPIER_JET
    jet_lf_mass = cal_fuel_mass(jet_dry_mass, jet_isp, jet_dv)
    jet_total_mass = jet_dry_mass + jet_lf_mass
    print("Jet(RAPIERs in airbreath mode):")
    print(f"Total mass: {jet_total_mass}t")
    print(f"LF mass: {jet_lf_mass}t")

    total_lf_mass = lko_lf_mass + jet_lf_mass + \
        rocket_lfo_mass * LFO_RATIO / (1 + LFO_RATIO)
    total_ox_mass = rocket_lfo_mass / (1 + LFO_RATIO)

    total_fuel_mass = total_lf_mass + total_ox_mass
    tanks_dry_mass = total_fuel_mass / 8

    engines_mass = n_nervs * MASS_NERV + n_rapiers * MASS_RAPIER

    payload_mass = jet_total_mass - tanks_dry_mass - \
        engines_mass - total_fuel_mass

    print()
    print("Summary:")
    print(f"Total mass: {jet_total_mass:.2f}t")
    print(f"Engines mass: {engines_mass}t")
    print(f"Tanks dry mass: {tanks_dry_mass:.2f}t")
    print(f"LF mass: {total_lf_mass:.2f}t, Unit: {int(total_lf_mass*200)}")
    print(f"Ox mass: {total_ox_mass:.2f}t, Unit: {int(total_ox_mass*200)}")
    print(f"Init TWR: {n_rapiers*THRUST_RAPIER_JET_M0/g/jet_total_mass:.2f}")
    print(f"Payload mass: {payload_mass:.2f}t")


def main():
    do_some_math(2, 4, 0.3, 4000)


if __name__ == '__main__':
    main()
