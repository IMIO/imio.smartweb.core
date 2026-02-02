import React from "react";
import { Translate, Translator } from "react-translated";
import { components } from "react-select";

/**
 * Composant ClearIndicator personnalisé pour react-select
 * Rend le bouton de suppression accessible au clavier
 * Utilisable avec la navigation Tab et activable avec Enter ou Espace
 */
const AccessibleClearIndicator = (props) => {
    const {
        children = components.ClearIndicator(props),
        innerProps: { ref, ...restInnerProps },
    } = props;
    return (
        <Translator>
            {({ translate }) => (
                <div
                    {...restInnerProps}
                    ref={ref}
                    tabIndex={0}
                    role="button"
                    aria-label={translate({ text: "Effacer la sélection" })}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            restInnerProps.onMouseDown(e);
                        }
                    }}
                >
                    {children}
                </div>
            )}
        </Translator>
    );
};

export default AccessibleClearIndicator;
