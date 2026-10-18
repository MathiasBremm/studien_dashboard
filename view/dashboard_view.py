import pandas as pd
import streamlit as st

from datetime import date, datetime
from dto.modul_eintrag_dto import ModulEintragDTO
from dto.dashboard_daten_dto import DashboardDatenDTO
from controller.dashboard_controller import DashboardController

# Full-Width Layout erzwingen
st.set_page_config(
    page_title="Studien-Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
    )

class DashboardView:
    """View-Klasse: Zuständig für die exakte Streamlit-Darstellung gemäß Layout-Skizze."""

    def zeige_dashboard(self, daten: DashboardDatenDTO, controller: DashboardController) -> None:

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
                f"Student: {daten.student_name} | "
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
            with st.container(border=True, height=290):
                # 1. Zeile: Notendurchschnitt (Label links, Wert rechts)
                col_label1, col_wert1 = st.columns([1.5, 1])
                with col_label1:
                    st.write("")  # Vertikaler Ausgleich
                    st.markdown("### Notendurchschnitt:")
                with col_wert1:
                    st.metric(
                        label="Notendurchschnitt",
                        value=f"{daten.aktueller_durchschnitt:.1f}".replace(".", ","),
                        label_visibility="collapsed",
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
                        label="Notentendenz",
                        value=f"{daten.notentrend:.1f}".replace(".", ","),
                        delta=delta,
                        delta_color="normal",
                        label_visibility="collapsed",
                    )

        # Rechte Kachel: Studienfortschritt & ECTS
        with col_kachel_rechts:
            with st.container(border=True, height=290):
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

            modul_eintrag = []
            for semester in daten.semester_liste:
                for m in semester.module:
                    p = m.pruefungsleistungen[-1] if m.pruefungsleistungen else None

                    note_val = float(p.note) if (p is not None and p.note is not None) else None
                    versuch_val = int(p.versuch) if p else 1
                    datum_val = p.datum if (p and p.datum) else None
                    abgabe_val = p.abgabe if (p and p.abgabe) else None

                    modul_eintrag.append(
                        {
                            "Semester": semester.nummer,
                            "Modulcode": m.modul_code,
                            "Modulname": m.name,
                            "ECTS": m.ects,
                            "Status": m.status.value,
                            "Note": note_val,
                            "Versuche": versuch_val,
                            "Abgabe": abgabe_val,
                            "Notendatum": datum_val,
                        }
                    )


            spalten_config = {
                "Semester": st.column_config.NumberColumn(
                    "Semester", min_value=1, max_value=9, step=1, format="%d", required=True
                ),
                "Modulcode": st.column_config.TextColumn("Modulcode", required=True),
                "Modulname": st.column_config.TextColumn("Modulname", required=True),
                "ECTS": st.column_config.NumberColumn(
                    "ECTS", min_value=1, max_value=50, step=1, format="%d", required=True
                ),
                "Note": st.column_config.NumberColumn(
                    "Note", min_value=1.0, max_value=5.0, step=0.1, format="%.1f"
                ),
                "Versuche": st.column_config.NumberColumn(
                    "Versuche", min_value=0, max_value=9, step=1, format="%d"
                ),
                "Abgabe": st.column_config.DateColumn("Abgabe", format="DD.MM.YYYY"),
                "Notendatum": st.column_config.DateColumn("Notendatum", format="DD.MM.YYYY"),
                "Status": st.column_config.TextColumn(
                    "Status", disabled=True, help="Wird beim Speichern automatisch ermittelt."
                ),
            }

            df = pd.DataFrame(modul_eintrag)

            edited_df = st.data_editor(
                df,
                column_config=spalten_config,
                width="stretch",
                hide_index=True,
                num_rows="dynamic",
                disabled=["Status"],
                key="modul_editor",
            )

            if st.button("Änderungen speichern", type="primary"):
                # DataFrame in neutrale DTO-Liste für den Controller umwandeln
                dto_module: list[ModulEintragDTO] = []
                for _, row in edited_df.iterrows():
                    if pd.isna(row.get("Modulcode")) or pd.isna(row.get("Semester")):
                        continue

                    note_raw = row.get("Note")
                    note_val = float(note_raw) if pd.notna(note_raw) and note_raw is not None else None
                    versuch_raw = row.get("Versuche")
                    versuch_val = int(versuch_raw) if pd.notna(versuch_raw) and versuch_raw is not None else 1

                    dto_module.append(
                        ModulEintragDTO(
                            semester=int(row["Semester"]),
                            modul_code=str(row.get("Modulcode", "")),
                            modul_name=str(row.get("Modulname", "")),
                            ects=int(row.get("ECTS", 5)),
                            status=str(row.get("Status", "OFFEN")),
                            note=note_val,
                            versuche=versuch_val,
                            abgabe=self._zu_datum(row.get("Abgabe")),
                            notendatum=self._zu_datum(row.get("Notendatum")),
                        )
                    )

                # Neutrale DTOs an Controller übergeben (Controller bleibt frei von pandas)
                controller.speichere_dashboard_daten(dto_module)
                st.success("Erfolgreich gespeichert!")
                st.rerun()

    @staticmethod
    def _zu_datum(wert) -> Optional[date]:
        if pd.isna(wert) or wert is None:
            return None
        if isinstance(wert, (datetime, pd.Timestamp)):
            return wert.date()
        if isinstance(wert, date):
            return wert
        if isinstance(wert, str) and wert.strip():
            try:
                return datetime.strptime(wert.strip(), "%Y-%m-%d").date()
            except ValueError:
                return None
        return None