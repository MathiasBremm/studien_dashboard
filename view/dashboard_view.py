import pandas as pd
import streamlit as st
from dto.dashboard_daten_dto import DashboardDatenDTO

# Full-Width Layout erzwingen
st.set_page_config(
    page_title="Studien-Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
    )

class DashboardView:
    """View-Klasse: Zuständig für die exakte Streamlit-Darstellung gemäß Layout-Skizze."""

    def zeige_dashboard(self, daten: DashboardDatenDTO) -> None:

        # ---------------------------------------------------------
        # 1. HEADER-BEREICH (Obere Box)
        # ---------------------------------------------------------
        with st.container(border=True):
            col_titel, col_ziel = st.columns([3, 1])
            with col_titel:
                st.subheader(
                    f"Studien-Dashboard - {daten.studiengang_name}"
                )
            with col_ziel:
                st.markdown(
                    f"**Notenziel:** {daten.ziel_durchschnitt:.1f}"
                )

            st.text(
                f"Student: Mathias Bremm | "
                f"Aktuelles Semester: {daten.aktuelles_semester}/{daten.letztes_semester} |" 
                f"Verstrichene Zeit: {daten.verstrichene_zeit_prozent}%"
                )
            st.text(f"Studienbeginn: {daten.studienbeginn}")

        st.write("")  # Vertikaler Abstand

        # ---------------------------------------------------------
        # 2. MITTLERE KACHELN (Gezielt getrennt in 2 Boxen)
        # ---------------------------------------------------------
        col_kachel_links, col_kachel_rechts = st.columns(2)

        # Linke Kachel: Notenübersicht
        with col_kachel_links:
            with st.container(border=True):
                # 1. Zeile: Notendurchschnitt (Label links, Wert rechts)
                col_label1, col_wert1 = st.columns([1.5, 1])
                with col_label1:
                    st.write("")  # Vertikaler Ausgleich
                    st.markdown("### Notendurchschnitt:")
                with col_wert1:
                    st.metric(
                        label="",
                        value=f"{daten.aktueller_durchschnitt:.1f}".replace(".", ","),
                    )

                st.divider()  # Dezente Trennlinie zwischen den Werten

                if daten.trend_delta is not None:
                    delta = f"{daten.trend_delta:+.1f}".replace(".", ",")
                else:
                    delta = None

                # 2. Zeile: Notentendenz (Label links, Wert/Metric rechts)
                col_label2, col_wert2 = st.columns([1.5, 1])
                with col_label2:
                    st.write("")  # Vertikaler Ausgleich
                    st.markdown("### Notentendenz:")
                with col_wert2:
                    st.metric(
                        label="",
                        value=f"{daten.notentrend:.1f}".replace(".", ","),
                        delta=delta,
                        delta_color="normal",
                    )

        # Rechte Kachel: Studienfortschritt & ECTS
        with col_kachel_rechts:
            with st.container(border=True):
                st.markdown("### Studienfortschritt:")
                st.markdown(
                    f"##### Gesamt-ECTS: {daten.absolvierte_ects}/{daten.gesamt_ects}"
                )
                st.progress(
                    daten.absolvierte_ects / daten.gesamt_ects
                )

                st.write("")
                st.markdown(
                    f"##### ECTS pro Semester (Soll: {daten.ects_soll_tempo} ECTS/Sem.)"
                )
                st.markdown(
                    f"## {daten.ects_ist_tempo:.1f}".replace(".", ",") + " ECTS/Sem.",
                )

        st.write("")  # Vertikaler Abstand

        # ---------------------------------------------------------
        # 3. UNTERE KACHEL (Modulübersicht & Prüfungen)
        # ---------------------------------------------------------
        with st.container(border=True):
            st.subheader("Modulübersicht & Prüfungen")

            modul_zeilen = []
            for semester in daten.semester_liste:
                for m in semester.module:
                    note_str = "-"
                    versuch_str = "-"
                    datum_str = "-"

                    if m.pruefungsleistungen:
                        p = m.pruefungsleistungen[-1]
                        if p.note is not None:
                            note_str = str(p.note).replace(".", ",")
                        versuch_str = str(p.versuch)
                        if p.datum:
                            datum_str = p.datum.strftime("%d.%m.%Y")

                    modul_zeilen.append(
                        {
                            "Modulcode": m.modul_code,
                            "Modulname": m.name,
                            "ECTS": m.ects,
                            "Status": m.status.value,
                            "Note": note_str,
                            "Versuche": versuch_str,
                            "Abgabe": "-",
                            "Notendatum": datum_str,
                        }
                    )

            if modul_zeilen:
                st.dataframe(
                    pd.DataFrame(modul_zeilen),
                    use_container_width=True,
                    hide_index=True,
                )