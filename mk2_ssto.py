#! /usr/bin/env python
"""
Long range Mk2 SSTO calculator
"""
import argparse
import math


parser = argparse.ArgumentParser(description='Mk2 SSTO calculator')
parser.add_argument(
    '--nervs',
    type=int,
    default=2,
    help='num of nuclear engines'
)
parser.add_argument(
    '--rapiers',
    type=int,
    default=4,
    help='num of RAPIERs'
)
parser.add_argument(
    '--lko-twr',
    type=float,
    default=0.24,
    help='TWR after reaching LKO'
)
parser.add_argument(
    '--lko-deltav',
    type=int,
    default=5000,
    help='deltaV remaining after reaching LKO'
)


KG = 9.81  # surface gravity of Kerbin

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

LFO_RATIO = 9/11


def cal_fuel_mass(dry_mass: float, isp: float, target_dv: float) -> float:
    """
    Calculate how much fuel is needed to attain a certain deltaV,
    """
    mass_ratio = math.e ** (target_dv / isp / KG)
    total_mass = dry_mass * mass_ratio
    return total_mass - dry_mass


def cal_dry_mass(init_mass: float, isp: float, target_dv: float) -> float:
    """
    Calculate how much dry mass is left to attain a certain deltaV
    """
    mass_ratio = math.e ** (target_dv / isp / KG)
    return init_mass / mass_ratio


def do_some_math(n_nervs: int, n_rapiers: int, lko_twr: float, lko_dv: float):
    # we need more deltaV to final accelerate and circlarize orbit
    bonus_dv = 400

    lko_total_mass = n_nervs * THRUST_NERV_VAC / lko_twr / KG
    lko_dry_mass = cal_dry_mass(lko_total_mass, ISP_NERV_VAC, lko_dv+bonus_dv)
    lko_lf_mass = lko_total_mass - lko_dry_mass
    # print("LKO:")
    # print(f"Total mass: {lko_total_mass:.2f}t")
    # print(f"Dry mass: {lko_dry_mass:.2f}t")
    # print(f"LF mass: {lko_lf_mass:.2f}t")
    # print()

    rocket_dry_mass = lko_total_mass
    rocket_dv = 550
    rocket_isp = ISP_RAPIER_ROCKET_VAC
    rocket_lfo_mass = cal_fuel_mass(rocket_dry_mass, rocket_isp, rocket_dv)
    rocket_lf_mass = rocket_lfo_mass * LFO_RATIO / (1 + LFO_RATIO)
    rocket_ox_mass = rocket_lfo_mass - rocket_lf_mass
    rocket_total_mass = rocket_dry_mass + rocket_lfo_mass
    # print("Rocket(RAPIERs closedcycle mode):")
    # print(f"Total mass: {rocket_total_mass:.2f}t")
    # print(f"LFO mass: {rocket_lfo_mass:.2f}t")
    # print()

    jet_dry_mass = rocket_total_mass
    air_drag_loss = 1000  # empirical value
    gravity_loss = 300    # empirical value
    jet_dv = 1500 + air_drag_loss + gravity_loss
    jet_isp = ISP_RAPIER_JET
    jet_lf_mass = cal_fuel_mass(jet_dry_mass, jet_isp, jet_dv)
    jet_total_mass = jet_dry_mass + jet_lf_mass
    # print("Jet(RAPIERs airbreath mode):")
    # print(f"Total mass: {jet_total_mass:.2f}t")
    # print(f"LF mass: {jet_lf_mass:.2f}t")
    # print()

    total_lf_mass = lko_lf_mass + jet_lf_mass + rocket_lf_mass
    total_ox_mass = rocket_ox_mass
    total_lf_units = int(total_lf_mass * 200)
    total_ox_units = int(total_ox_mass * 200)

    total_fuel_mass = total_lf_mass + total_ox_mass
    tanks_dead_mass = total_fuel_mass / 8

    engines_mass = n_nervs * MASS_NERV + n_rapiers * MASS_RAPIER

    payload_mass = jet_total_mass - tanks_dead_mass - \
        engines_mass - total_fuel_mass

    init_twr = n_rapiers * THRUST_RAPIER_JET_M0 / KG / jet_total_mass

    print(f"Total mass:      {jet_total_mass:.2f}t")
    print(f"Init TWR:        {init_twr:.2f}")
    print(f"Engines mass:    {engines_mass}t")
    print(f"Tanks dead mass: {tanks_dead_mass:.2f}t")
    print(f"LF mass:         {total_lf_mass:.2f}t ({total_lf_units} units)")
    print(f"Ox mass:         {total_ox_mass:.2f}t ({total_ox_units} units)")
    print(f"Payload mass:    {payload_mass:.2f}t")


def main():
    """
    main
    """
    args = parser.parse_args()
    do_some_math(args.nervs, args.rapiers, args.lko_twr, args.lko_deltav)


if __name__ == '__main__':
    main()
