##############################################################################
#  Copyright (C) 2015 Ronald Portier <ronald.portier.eu>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################
from pprint import pprint

# Belastingsoorten
OZB_BEW = 'ozb_bewoners'
OZB_GEB = 'ozb gebruikers (zakelijk)'
OZB_EIG = 'ozb eigenaren (zakelijk)'
AFH_BEW = 'afvalstoffenheffing (bewoners)'
RH_BEW = 'rioolheffing (bewoners)'
RH_EIG = 'rioolheffing (eigenaren woningen)'

# In de cijfers over opbrengsten van de rioolheffing wordt geen onderscheid
# gemaakt tussen de rioolheffing eigenaren en rioolheffing bewoners.
RH_TOT = 'rioolheffing (totaal woningen)'

# In de begroting is alleen een totaalbedrag voor de opbrengst van de ozb
# te vinden.
OZB_TOT = 'ozb totaal'

# Tarieven 2014 en 2015 van website gemeente en verordeningen (ris)
# Opbrengsten 2014 uit de jaarrekening
# Opbrengsten 2015 uit de begroting

# De tarieven voor de ozb zijn percentages. De overige vaste bedragen.

# Tarieven 2014
tarieven_2014 = {
    OZB_BEW: 0.1280,
    OZB_EIG: 0.2386,
    OZB_GEB: 0.1913,
    AFH_BEW: 255.72,
    RH_BEW: 77.52,
    RH_EIG: 86.73,
}

# Tarieven 2014
tarieven_2015 = {
    OZB_BEW: 0.1322,
    OZB_EIG: 0.2506,
    OZB_GEB: 0.1979,
    AFH_BEW: 258.24,
    RH_BEW: 88.52,
    RH_EIG: 90.20,
}

# Opbrengsten 2014 (* 1.000,- euro):
opbrengsten_2014 = {
    OZB_BEW: 11158,
    OZB_EIG: 7139,
    OZB_GEB: 5169,
    AFH_BEW: 13344,
    RH_TOT: 10477,
}

# Opbrengsten 2015 (* 1.000,- euro):
opbrengsten_2015 = {
    OZB_TOT: 22641,
    AFH_BEW: 13456,
    RH_TOT:11142,
}


# Bereken totale OZB opbrengst 2014:
opbrengsten_2014[OZB_TOT] = (
    opbrengsten_2014[OZB_BEW] +
    opbrengsten_2014[OZB_EIG] +
    opbrengsten_2014[OZB_GEB]
)


def print_opbrengsten(jaar, opbrengsten):
    """Nette afdruk van de opbrengsten in een jaar."""
    print '==========================='
    print 'Opbrengsten %d:' % jaar
    pprint(opbrengsten)


def schat_verdeling(
        nieuw_jaar, vergelijkings_jaar, totaal_veld, deel_veld):
    """Als we voor een nieuw jaar alleen een totaal-opbrengst weten van een
    groep belastingen, dan kunnen we het aandeel van een afzonderlijke
    belasting schatten aan de hand van de verdeling in een vorig jaar."""
    return  int(round(
        float(nieuw_jaar[totaal_veld]) *
        (float(vergelijkings_jaar[deel_veld]) /
         float(vergelijkings_jaar[totaal_veld]))
    ))



def verdeling_voordeel_nadeel(tarieven_nieuw, tarieven_oud):
    """Druk voor verschillende groepen het voordelig saldo af voor
    twee tariefstructuren."""

    def voordeel_nadeel(saldo):
        return (
            (saldo > 0) and 'voordeel' or
            (saldo == 0) and 'gelijk' or 'nadeel'
        )

    print 'effect op huurders (uitgaande van geen doorbelasting)'
    saldo_heffingen_huurder = int(round(
        tarieven_nieuw[AFH_BEW] - tarieven_oud[AFH_BEW] +
        tarieven_nieuw[RH_BEW] - tarieven_oud[RH_BEW]
    )) * -1
    tekst_heffingen_huurder = voordeel_nadeel(saldo_heffingen_huurder)
    print "{th} heffingen huurder {sh}".format(
        th=tekst_heffingen_huurder, sh=saldo_heffingen_huurder,
    )
    print 'effect op bewoner-eigenaren'
    saldo_heffingen = int(round(
        tarieven_nieuw[AFH_BEW] - tarieven_oud[AFH_BEW] +
        tarieven_nieuw[RH_BEW] - tarieven_oud[RH_BEW] +
        tarieven_nieuw[RH_EIG] - tarieven_oud[RH_EIG]
    )) * -1
    tekst_heffingen = voordeel_nadeel(saldo_heffingen)
    for woz in [100000, 150000, 200000, 300000, 400000, 600000, 1000000]:
        saldo_ozb = int(round(
            (tarieven_nieuw[OZB_BEW] * woz) / 100 -
            (tarieven_oud[OZB_BEW] * woz) / 100
        )) * -1
        saldo_totaal = saldo_ozb + saldo_heffingen
        tekst_heffingen = voordeel_nadeel(saldo_heffingen)
        tekst_ozb = voordeel_nadeel(saldo_ozb)
        tekst_totaal = voordeel_nadeel(saldo_totaal)
        print (
            "Bij WOZ waarde {woz}, {th} heffingen {sh},"
            " {to} ozb {so}, totaal {tt} {st}.".format(
                woz=woz,
                th=tekst_heffingen, sh=saldo_heffingen,
                to=tekst_ozb, so=saldo_ozb,
                tt=tekst_totaal, st=saldo_totaal)
        )


def bereken_nieuwe_opbrengsten(
        tarieven_nieuw, tarieven_oud, opbrengsten_oud):
    """Bereken nieuwe opbrengsten uit de tariefswijziging en de oude
    opbrengsten. Hierbij gaan we ervanuit dat aantallen bewoners en
    gebruikers en woz waardes constant zijn: het gaat om het effect van de
    andere tarieven."""
    opbrengsten_nieuw = {}
    for key, value in opbrengsten_oud.items():
        if key in tarieven_nieuw and key in tarieven_oud:
            opbrengsten_nieuw[key] = int(round(
                float(value) *
                (float(tarieven_nieuw[key]) / float(tarieven_oud[key]))
            ))
    return opbrengsten_nieuw


def print_scenario(
        scenario, tarieven, tarieven_oud, opbrengsten, opbrengsten_oud):
    """Afdrukken van de tarieven en opbrengsten behorende bij een
    scenario."""
    print '======================================================='
    print scenario
    print 'Tarieven %s' % scenario
    pprint(tarieven)
    print 'Opbrengsten %s' % scenario
    pprint(opbrengsten)
    verdeling_voordeel_nadeel(tarieven, tarieven_oud)


def get_totaal_opbrengsten(opbrengsten):
    """Bereken totaal opbrengsten voor de afzonderlijke belastingen.
    
    Als totaal van belastingen in opbrengsten, dan die nemen, anders
    de losse belastingen.
    """
    totaal = 0
    key_list = [AFH_BEW]
    # Totaal rioolrechten ingevuld?
    if RH_TOT in opbrengsten and opbrengsten[RH_TOT]:
        key_list.append(RH_TOT)
    else:
        key_list += [RH_BEW, RH_EIG]
    # Totaal ozb ingevuld?
    if OZB_TOT in opbrengsten and opbrengsten[OZB_TOT]:
        key_list.append(OZB_TOT)
    else:
        key_list += [OZB_BEW, OZB_EIG, OZB_GEB]
    for key in key_list:
        if key in opbrengsten:
            totaal += opbrengsten[key] 
        else:
            print 'Geen %s in opbrengsten!' % key
    return totaal


# Schat afzonderlijke OZB opbrengsten 2015:
for ozb_onderdeel in [OZB_BEW, OZB_EIG, OZB_GEB]:
    opbrengsten_2015[ozb_onderdeel] = schat_verdeling(
        opbrengsten_2015, opbrengsten_2014, OZB_TOT, ozb_onderdeel)

# Print feitelijke opbrengsten 2014:
print_opbrengsten(2014, opbrengsten_2014)

# Vergelijk tarieven 2014 en 2015
print_scenario(
    'van 2014 naar 2015', tarieven_2015, tarieven_2014,
    opbrengsten_2015, opbrengsten_2014
)

# ================= Scenario 01 ========================================= #
# Scenario 01 AFH en RH worden vervangen door ozb, ozb over alle groepen
factor_ozb_scenario_01 = round(
    (
        float(opbrengsten_2015[OZB_TOT] +
              opbrengsten_2015[AFH_BEW] +
              opbrengsten_2015[RH_TOT]
             ) / float(opbrengsten_2015[OZB_TOT])
    ), 2
)
print (
    "Factor verhoging ozb, bij verdeling heffingen over alle ozb tarieven"
    " = %.2f" % factor_ozb_scenario_01
)
tarieven_scenario_01 = {
    AFH_BEW: 0.0,
    RH_BEW: 0.0,
    RH_EIG: 0.0,
}
for tarief in [OZB_BEW, OZB_EIG, OZB_GEB]:
    tarieven_scenario_01[tarief] = round(
        (factor_ozb_scenario_01 * tarieven_2015[tarief]),
        4
    )
opbrengsten_scenario_01 = bereken_nieuwe_opbrengsten(
    tarieven_scenario_01, tarieven_2015, opbrengsten_2015
)
print_scenario(
    'scenario01', tarieven_scenario_01, tarieven_2015,
    opbrengsten_scenario_01, opbrengsten_2015
)

# ================= Scenario 02 ========================================= #
# Scenario 02 RH worden vervangen door ozb, ozb over alle groepen
factor_ozb_scenario_02 = round(
    (
        float(opbrengsten_2015[OZB_TOT] +
              opbrengsten_2015[RH_TOT]
             ) / float(opbrengsten_2015[OZB_TOT])
    ), 2
)
print (
    "Factor verhoging ozb, bij verdeling rioolheffing over alle ozb tarieven"
    " = %.2f" % factor_ozb_scenario_02
)
tarieven_scenario_02 = {
    AFH_BEW: tarieven_2015[AFH_BEW],
    RH_BEW: 0.0,
    RH_EIG: 0.0,
}
for tarief in [OZB_BEW, OZB_EIG, OZB_GEB]:
    tarieven_scenario_02[tarief] = round(
        (factor_ozb_scenario_02 * tarieven_2015[tarief]),
        4
    )
opbrengsten_scenario_02 = bereken_nieuwe_opbrengsten(
    tarieven_scenario_02, tarieven_2015, opbrengsten_2015
)
print_scenario(
    'scenario 02', tarieven_scenario_02, tarieven_2015,
    opbrengsten_scenario_02, opbrengsten_2015
)

# ================= Scenario 03 ========================================= #
# Scenario 03 RH weg, Nijmeegse tarieven OZB. Rest is AFH
tarieven_scenario_03 = {
    AFH_BEW: 0.0,
    RH_BEW: 0.0,
    RH_EIG: 0.0,
    OZB_BEW: 0.2413,
    OZB_EIG: 0.4504,
    OZB_GEB: 0.3491,
}
# Bereken opbrengsten eerst uit zonder AFH
opbrengsten_scenario_03 = bereken_nieuwe_opbrengsten(
    tarieven_scenario_03, tarieven_2015, opbrengsten_2015
)
# Bereken benodigd tarief AFH uit tekort aan opbrengsten als geen
# AFH wordt berekend:
opbrengsten_2015_totaal = get_totaal_opbrengsten(opbrengsten_2015)
print 'Totaal opbrengsten 2015 %d' % opbrengsten_2015_totaal
opbrengsten_scenario_03_totaal = get_totaal_opbrengsten(
    opbrengsten_scenario_03)
print 'Totaal opbrengsten scenario 03 zonder AFH %d' % (
    opbrengsten_scenario_03_totaal)
opbrengsten_scenario_03[AFH_BEW] = (
    opbrengsten_2015_totaal - opbrengsten_scenario_03_totaal)
opbrengsten_scenario_03_totaal = get_totaal_opbrengsten(
    opbrengsten_scenario_03)
print 'Totaal opbrengsten scenario 03 met AFH %d' % (
    opbrengsten_scenario_03_totaal)
tarieven_scenario_03[AFH_BEW] = round(
    tarieven_2015[AFH_BEW] *
    (float(opbrengsten_scenario_03[AFH_BEW]) /
     float(opbrengsten_2015[AFH_BEW])
    ),
    2
)
print_scenario(
    'scenario 03', tarieven_scenario_03, tarieven_2015,
    opbrengsten_scenario_03, opbrengsten_2015
)
