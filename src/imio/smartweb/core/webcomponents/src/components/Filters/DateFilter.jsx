import React, { useEffect, useRef, useCallback, useState } from "react";
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import moment from "moment";
import { Dropdown, DropdownButton } from 'react-bootstrap';

function DateFilter({ setDates }) {

    const [startDate, setStartDate] = useState(new Date());
    const [endDate, setEndDate] = useState(new Date());
    const [filter, setFilter] = useState('Période');
    const handleApply = () => {
        const start = moment(startDate).format('YYYY-MM-DD');
        const end = moment(endDate).format('YYYY-MM-DD');
        setDates({ "event_dates.query": [start, end] });
        setFilter(`custom`);
    };
    const today = moment().format('YYYY-MM-DD');
    const handleSelect = (eventKey) => {
        switch (eventKey) {
            case 'today':
                setDates({ "event_dates.query": [today, today] });
                setFilter("Aujourd'hui");
                break;
            case 'tomorrow':
                const tomorrow = moment().add(1, 'days').format('YYYY-MM-DD');
                setDates({ "event_dates.query": [tomorrow, tomorrow] });
                setFilter('Demain');
                break;
            case 'thisWeekEnd':
                const startOfWeekEnd = moment().endOf('week').format('YYYY-MM-DD');
                const endOfWeekEnd = moment().endOf('week').add(1, 'days').format('YYYY-MM-DD');
                setDates({ "event_dates.query": [startOfWeekEnd, endOfWeekEnd] });
                setFilter('Ce week-end');
                break;
            case 'thisWeek':
                const endOfWeek = moment().endOf('week').add(1, 'days').format('YYYY-MM-DD');
                setDates({ "event_dates.query": [today, endOfWeek] });
                setFilter('Cette semaine');
                break;
            case 'thisMonth':
                const endOfMonth = moment().endOf('month').format('YYYY-MM-DD');
                setDates({ "event_dates.query": [today, endOfMonth] });
                setFilter('Cette semaine');
                break;
            default:
                break;
        }
    };
    //  2023-02-23

    return (
        <>
            <div>
                <DropdownButton onSelect={handleSelect} title={filter}>
                    <Dropdown.Item eventKey="today">Aujourd'hui</Dropdown.Item>
                    <Dropdown.Item eventKey="tomorrow">Demain</Dropdown.Item>
                    <Dropdown.Item eventKey="thisWeekEnd">Ce week-end</Dropdown.Item>
                    <Dropdown.Item eventKey="thisWeek">Cette semaine</Dropdown.Item>
                    <Dropdown.Item eventKey="thisMonth">Ce mois-ci</Dropdown.Item>

                    <div>
                        du
                        <DatePicker
                            selected={startDate}
                            onChange={(date) => setStartDate(date)}
                            selectsStart
                            startDate={startDate}
                            endDate={endDate}
                            onClick={(e) => e.stopPropagation()}
                        />
                        au
                        <DatePicker
                            selected={endDate}
                            onChange={(date) => setEndDate(date)}
                            selectsEnd
                            startDate={startDate}
                            endDate={endDate}
                            minDate={startDate}
                            onClick={(e) => e.stopPropagation()}
                        />
                        <button
                            onClick={(e) => {
                                e.stopPropagation();
                                handleApply()
                            }}
                        >
                            Valider
                        </button>
                        {/* <button onClick={handleApply}>Apply</button> */}
                    </div>
                </DropdownButton>
            </div>
        </>
    );
}

export default DateFilter;
