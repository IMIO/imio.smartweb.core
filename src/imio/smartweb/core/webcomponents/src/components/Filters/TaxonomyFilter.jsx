import React, { useState, useEffect } from "react";
import Select from "react-select";
import "./TaxonomyFilter.scss";

function TaxonomyFilter({ onChange, sub, title, token, isActive, setCat, onClick }) {
    const [select1Value, setSelect1Value] = useState(null);
    const [select2Value, setSelect2Value] = useState(null);
    const [select3Value, setSelect3Value] = useState(null);
    const [firstLevelOptions, setFirstLevelOptions] = useState(null);
    const [secondLevelOptions, setSecondLevelOptions] = useState(null);
    // État pour suivre l'affichage de la div associée
    const [secondLevelVisible, setsecondLevelVisible] = useState(false);
    const [thirdLevelVisible, setThirdLevelVisible] = useState(false);
    //  const avev la valeur des filtres
    const [filterValue, setFilterValue] = useState({
        taxonomy_contact_category_for_filtering: null,
    });

    // Object { b_start: "0", fullobjects: "1", taxonomy_contact_category_for_filtering: "ol8av3v8bn" }

    // Dans le composant TaxonomyFilter
    useEffect(() => {
        if (!isActive) {
            setsecondLevelVisible(false);
            setThirdLevelVisible(false);
            setSelect2Value(null);
        }
    }, [isActive]);

    useEffect(() => {
        if (sub) {
            const optionsSub1 = sub.map((d) => ({
                value: d.token,
                label: d.title,
                ...(d.sub && { sub: d.sub }),
            }));
            setFirstLevelOptions(optionsSub1);
        }
    }, [sub]);
    // Gestionnaire d'événements pour le clic sur le lien
    const handleLinkClick = () => {
        // Inverser la valeur de l'état pour afficher ou masquer la div
        setsecondLevelVisible(!secondLevelVisible);
        setSelect2Value(null);
        setThirdLevelVisible(false);
    };

    // Gestionnaire d'événements pour le changement de valeur dans le premier select
    const onChangeSub1 = (value, action) => {
        if (value && value.sub) {
            const optionsSub2 = value.sub.map((d) => ({
                value: d.token,
                label: d.title,
            }));
            setSelect2Value(value.label);
            setSelect3Value(null);
            setSecondLevelOptions(optionsSub2);
            setThirdLevelVisible(true);
            onChange(value, action);
        } else {
            setSecondLevelOptions(null);
        }
    };

    // Gestionnaire d'événements pour le changement de valeur dans le deuxième select
    const onChangeSub2 = (value, action) => {
        setSelect3Value(value.label);
        onChange(value, action);
    };

    // send the value to the first level (a link)
    const handleApply = (value, title) => {
        setCat((prevCat) => !prevCat);
        if (!secondLevelVisible) {
            onChange(
                { value: value, label: title },
                { name: "taxonomy_contact_category_for_filtering" }
            );
        } else {
            onChange(null, { name: "taxonomy_contact_category_for_filtering" });
        }
    };

    return (
        <div onClick={onClick}>
            <div
                className={
                    secondLevelVisible ? "dropDownFilter dropDownFilter-active" : "dropDownFilter"
                }
            >
                {/* Lien avec gestionnaire d'événements */}
                <a
                    className="sub0"
                    href="#"
                    value={title}
                    onClick={(e) => {
                        e.preventDefault();
                        handleLinkClick();
                        handleApply(token, title); // Pass the correct value to handleApply
                    }}
                >
                    {title}
                </a>

                {/* Div conditionnellement rendue en fonction de l'état */}
                {firstLevelOptions && (
                    <div
                        className={
                            secondLevelVisible
                                ? "sub1 dropDownFilter-visible"
                                : "sub1 dropDownFilter-invisble"
                        }
                    >
                        <Select
                            name={"taxonomy_contact_category_for_filtering"}
                            className="select-custom-class library-facilities"
                            onChange={onChangeSub1}
                            options={firstLevelOptions}
                            value={select2Value}
                            placeholder={select2Value ? select2Value : "Catégories"}
                        />
                    </div>
                )}

                {/* Div 3 conditionnellement rendue en fonction de l'état */}
                {secondLevelOptions && (
                    <div
                        className={
                            thirdLevelVisible
                                ? "sub2 dropDownFilter-visible"
                                : "sub2 dropDownFilter-invisble"
                        }
                    >
                        <Select
                            name={"taxonomy_contact_category_for_filtering"}
                            className="select-custom-class library-facilities"
                            onChange={onChangeSub2}
                            options={secondLevelOptions}
                            value={select3Value}
                            placeholder={select3Value ? select3Value : "Catégories"}
                        />
                    </div>
                )}
            </div>
        </div>
    );
}

export default TaxonomyFilter;
