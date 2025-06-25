import React, { useState, useEffect, useMemo, useCallback } from "react";
import PropTypes from "prop-types";
import Select from "react-select";
import "./TaxonomyFilter.scss";

function TaxonomyFilter({ onChange, sub, title, token, isActive, setCat, onClick }) {
    // Regroupement des états liés
    const [selectValues, setSelectValues] = useState({
        first: null,
        second: null,
        third: null,
    });

    const [visibility, setVisibility] = useState({
        secondLevel: false,
        thirdLevel: false,
    });

    const [options, setOptions] = useState({
        firstLevel: null,
        secondLevel: null,
    });

    // Mémoisation des options du premier niveau
    const firstLevelOptions = useMemo(() => {
        if (!sub) return null;
        return sub.map((d) => ({
            value: d.token,
            label: d.title,
            ...(d.sub && { sub: d.sub }),
        }));
    }, [sub]);

    // Gestionnaires d'événements avec useCallback
    const handleLinkClick = useCallback(() => {
        setVisibility((prev) => ({
            secondLevel: !prev.secondLevel,
            thirdLevel: false,
        }));
        setSelectValues((prev) => ({
            ...prev,
            second: null,
            third: null,
        }));
    }, []);

    const onChangeSub1 = useCallback(
        (value, action) => {
            // console.log(value);
            if (value?.sub) {
                const secondLevelOptions = value.sub.map((d) => ({
                    value: d.token,
                    label: d.title,
                }));
                setSelectValues((prev) => ({
                    ...prev,
                    second: value.label,
                    third: null,
                }));
                setOptions((prev) => ({
                    ...prev,
                    secondLevel: secondLevelOptions,
                }));
                setVisibility((prev) => ({
                    ...prev,
                    thirdLevel: true,
                }));
                onChange(value, action);
            } else {
                setSelectValues((prev) => ({
                    ...prev,
                    second: value.label,
                    third: null,
                }));
                setOptions((prev) => ({
                    ...prev,
                    secondLevel: null,
                }));
                onChange(value, action);
            }
        },
        [onChange]
    );

    const onChangeSub2 = useCallback(
        (value, action) => {
            setSelectValues((prev) => ({
                ...prev,
                third: value.label,
            }));
            onChange(value, action);
        },
        [onChange]
    );

    const handleApply = useCallback(
        (value, title) => {
            setCat((prev) => !prev);
            if (!visibility.secondLevel) {
                onChange(
                    { value, label: title },
                    { name: "taxonomy_contact_category_for_filtering" }
                );
            } else {
                onChange(null, { name: "taxonomy_contact_category_for_filtering" });
            }
        },
        [visibility.secondLevel, onChange, setCat]
    );

    // Effet pour réinitialiser l'état quand isActive change
    useEffect(() => {
        if (!isActive) {
            setVisibility({
                secondLevel: false,
                thirdLevel: false,
            });
            setSelectValues((prev) => ({
                ...prev,
                second: null,
                third: null,
            }));
        }
    }, [isActive]);

    // Effet pour mettre à jour les options du premier niveau
    useEffect(() => {
        if (sub) {
            setOptions((prev) => ({
                ...prev,
                firstLevel: firstLevelOptions,
            }));
        }
    }, [sub, firstLevelOptions]);

    return (
        <div onClick={onClick}>
            <div
                className={
                    visibility.secondLevel
                        ? "dropDownFilter dropDownFilter-active"
                        : "dropDownFilter"
                }
            >
                <a
                    className="sub0"
                    href="#"
                    value={title}
                    onClick={(e) => {
                        e.preventDefault();
                        handleLinkClick();
                        handleApply(token, title);
                    }}
                >
                    {title}
                </a>

                {options.firstLevel && (
                    <div
                        className={
                            visibility.secondLevel
                                ? "sub1 dropDownFilter-visible"
                                : "sub1 dropDownFilter-invisble"
                        }
                    >
                        <Select
                            name="taxonomy_contact_category_for_filtering"
                            className={`select-custom-class library-facilities react-select-container ${
                                selectValues.second && selectValues.second !== "Catégories"
                                    ? "select-has-value"
                                    : ""
                            }`}
                            classNamePrefix="react-select-custom-multi"
                            onChange={onChangeSub1}
                            options={options.firstLevel}
                            value={selectValues.second}
                            placeholder={selectValues.second ? selectValues.second : "Catégories"}
                        />
                    </div>
                )}

                {options.secondLevel && (
                    <div
                        className={
                            visibility.thirdLevel
                                ? "sub2 dropDownFilter-visible"
                                : "sub2 dropDownFilter-invisble"
                        }
                    >
                        <Select
                            name="taxonomy_contact_category_for_filtering"
                            className={`react-custom-multi-select-container library-facilities ${
                                selectValues.third && selectValues.third !== "Catégories"
                                    ? "select-has-value"
                                    : ""
                            }`}
                            classNamePrefix="react-select-custom-multi"
                            onChange={onChangeSub2}
                            options={options.secondLevel}
                            value={selectValues.third}
                            placeholder={selectValues.third ? selectValues.third : "Catégories"}
                        />
                    </div>
                )}
            </div>
        </div>
    );
}

TaxonomyFilter.propTypes = {
    onChange: PropTypes.func.isRequired,
    sub: PropTypes.arrayOf(
        PropTypes.shape({
            token: PropTypes.string.isRequired,
            title: PropTypes.string.isRequired,
            sub: PropTypes.array,
        })
    ),
    title: PropTypes.string.isRequired,
    token: PropTypes.string.isRequired,
    isActive: PropTypes.bool,
    setCat: PropTypes.func.isRequired,
    onClick: PropTypes.func,
};

TaxonomyFilter.defaultProps = {
    isActive: false,
    onClick: () => {},
};

export default TaxonomyFilter;
