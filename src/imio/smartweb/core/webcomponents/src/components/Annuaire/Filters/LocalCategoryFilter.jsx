import React from "react";
import PropTypes from "prop-types";
import Select from "react-select";
import { Translator } from "react-translated";
import AccessibleClearIndicator from "../../../utils/AccessibleClearIndicator";

// "+" shown in place of the usual chevron, until a category is selected
const PlusIndicator = ({ innerProps, hasValue }) =>
    hasValue ? null : (
        <div
            {...innerProps}
            aria-hidden="true"
            style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "0 12px",
                fontSize: "1.2rem",
                lineHeight: 1,
            }}
        >
            +
        </div>
    );

const NoPlaceholder = () => null;

const styles = {
    control: (base, state) => ({
        ...base,
        // same height as the neighbouring category pills (.dropDownFilter)
        height: 36,
        minHeight: 36,
        fontSize: "0.75rem",
        cursor: "pointer",
        border: "solid 1px #cfcfcf",
        borderRadius: 15,
        boxShadow: state.isFocused ? "0 0 0 1px #2684ff" : "none",
        borderColor: state.isFocused ? "#2684ff" : "#cfcfcf",
    }),
    valueContainer: (base, state) => ({
        ...base,
        padding: state.hasValue ? "0 0 0 10px" : 0,
    }),
    menu: (base) => ({ ...base, width: "max-content", minWidth: "100%", maxWidth: 300 }),
};

function LocalCategoryFilter({ options, value, onChange }) {
    if (!options || options.length === 0) return null;

    const selected = options.find((option) => option.value === value) || null;

    return (
        <Translator>
            {({ translate }) => (
                <div className="local-category-filter">
                    <Select
                        name="local_category"
                        aria-label={translate({ text: "Catégories spécifiques" })}
                        classNamePrefix="react-select-local-category"
                        isClearable
                        isSearchable={false}
                        components={{
                            DropdownIndicator: PlusIndicator,
                            IndicatorSeparator: null,
                            Placeholder: NoPlaceholder,
                            ClearIndicator: AccessibleClearIndicator,
                        }}
                        styles={styles}
                        onChange={onChange}
                        options={options}
                        value={selected}
                    />
                </div>
            )}
        </Translator>
    );
}

LocalCategoryFilter.propTypes = {
    options: PropTypes.arrayOf(
        PropTypes.shape({ value: PropTypes.string, label: PropTypes.string })
    ),
    value: PropTypes.string,
    onChange: PropTypes.func.isRequired,
};

export default LocalCategoryFilter;
