import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import moment from "moment";
import { Dropdown, DropdownButton } from "react-bootstrap";
import { Translate, Translator } from "react-translated";
import { nl, fr, enGB, de } from "date-fns/locale";

import "./DateFilter.scss";

const languageList = {
    fr: fr,
    nl: nl,
    de: de,
    en: enGB,
};
function DateFilter({ language, setDates }) {
    const [dateRange, setDateRange] = useState([null, null]);
    const [startDate, endDate] = dateRange;
    const [filter, setFilter] = useState(<Translate text="Quand" />);
    const [languageToLocale, setLanguageToLocale] = useState();

    const handleApply = (e) => {
        setDateRange(e);
        const dates = e; // Remplacez ceci par votre tableau de dates
        const filteredDates = dates.filter((date) => date !== null);
        const formattedDates = filteredDates.map((date) => moment(date).format("YYYY-MM-DD"));
        setDates({ "event_dates.query": formattedDates });
        if (e.every((item) => item === null)) {
            setFilter(periodTitle.all);
        } else {
            setFilter(periodTitle.custom);
        }
    };
    const today = moment().format("YYYY-MM-DD");

    const periodTitle = {
        all: <Translate text="Toutes les dates" />,
        today: <Translate text="Aujourd'hui" />,
        tomorrow: <Translate text="Demain" />,
        thisWeekEnd: <Translate text="Ce week-end" />,
        thisWeek: <Translate text="Cette semaine" />,
        thisMonth: <Translate text="Ce mois-ci" />,
        custom: <Translate text="Personnalisé (Du ... au ...)" />,
    };

    const handleSelect = (eventKey) => {
        switch (eventKey) {
            case "all":
                setDates({ "event_dates.query": [today] });
                setFilter(periodTitle.all);
                break;
            case "today":
                setDates({ "event_dates.query": [today, today] });
                setFilter(periodTitle.today);
                break;
            case "tomorrow":
                const tomorrow = moment().add(1, "days").format("YYYY-MM-DD");
                setDates({ "event_dates.query": [tomorrow, tomorrow] });
                setFilter(periodTitle.tomorrow);
                break;
            case "thisWeekEnd":
                const startOfWeekEnd = moment().endOf("week").format("YYYY-MM-DD");
                const endOfWeekEnd = moment().endOf("week").add(1, "days").format("YYYY-MM-DD");
                setDates({ "event_dates.query": [startOfWeekEnd, endOfWeekEnd] });
                setFilter(periodTitle.thisWeekEnd);
                break;
            case "thisWeek":
                const endOfWeek = moment().endOf("week").add(1, "days").format("YYYY-MM-DD");
                setDates({ "event_dates.query": [today, endOfWeek] });
                setFilter(periodTitle.thisWeek);
                break;
            case "thisMonth":
                const endOfMonth = moment().endOf("month").format("YYYY-MM-DD");
                setDates({ "event_dates.query": [today, endOfMonth] });
                setFilter(periodTitle.thisMonth);
                break;
            default:
                break;
        }
    };

    useState(() => {
        setLanguageToLocale(languageList[language]);
    }, []);

    return (
        <>
            <div className="period-filter">
                <DropdownButton
                    className="period-filter-toggler"
                    onSelect={handleSelect}
                    title={filter}
                >
                    <Dropdown.Item eventKey="all">{periodTitle.all}</Dropdown.Item>
                    <Dropdown.Item eventKey="today">{periodTitle.today}</Dropdown.Item>
                    <Dropdown.Item eventKey="tomorrow">{periodTitle.tomorrow}</Dropdown.Item>
                    <Dropdown.Item eventKey="thisWeekEnd">{periodTitle.thisWeekEnd}</Dropdown.Item>
                    <Dropdown.Item eventKey="thisWeek">{periodTitle.thisWeek}</Dropdown.Item>
                    <Dropdown.Item eventKey="thisMonth">{periodTitle.thisMonth}</Dropdown.Item>
                    <div className="perdiod-filter-range">
                        {languageToLocale && (
                            <Translator>
                                {({ translate, language }) => (
                                    <DatePicker
                                        dateFormat="dd/MM/yyyy"
                                        placeholderText={translate({
                                            text: "Personnalisé (Du ... au ...)",
                                        })}
                                        selectsRange={true}
                                        startDate={startDate}
                                        endDate={endDate}
                                        minDate={new Date().setDate(new Date().getDate() + 1)}
                                        onChange={(update) => {
                                            setDateRange(update);
                                            if (
                                                (update[0] !== null && update[1] !== null) ||
                                                (update[0] == null && update[1] == null)
                                            ) {
                                                handleApply(update);
                                            }
                                        }}
                                        isClearable={true}
                                        locale={languageToLocale}
                                    />
                                )}
                            </Translator>
                        )}
                    </div>
                </DropdownButton>
            </div>
        </>
    );
}

export default DateFilter;
