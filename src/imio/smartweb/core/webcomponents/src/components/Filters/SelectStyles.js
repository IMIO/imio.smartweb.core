export const menuStyles = {
    control: (styles) => ({
        ...styles,
        backgroundColor: "white",
        borderColor: "transparent",
        borderRadius: "10px",
        minWidth:"150px",
        height: "40px",
    }),
    menu: (styles) => ({
        ...styles,
        width: "max-content",
        maxWidth: "250px",
    }),
    placeholder: (styles) => ({
        ...styles,
        color: "000",
        fontWeight: "bold",
        fontSize: "14px",
        letterSpacing: "1.4px",
    }),
    indicators: (styles) => ({
        ...styles,
        color: "blue",
    }),
    option: (styles) => {
        return {
            ...styles,
        };
    },
};

export const moreFilterStyles = {
    control: (styles) => ({
        ...styles,
        backgroundColor: "white",
        borderRadius: "10px",
        height: "30px",
        minWidth:"150px",
    }),
    placeholder: (styles) => ({
        ...styles,
        color: "000",
        fontWeight: "bold",
        fontSize: "12px",
        letterSpacing: "1.4px",
    }),
    menu: (styles) => ({
        ...styles,
        width: "max-content",
        maxWidth: "250px",
    }),
    option: (styles, { data, isDisabled, isFocused, isSelected }) => {
        return {
            ...styles,
        };
    },
};