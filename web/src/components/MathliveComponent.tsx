/* eslint-disable react-hooks/exhaustive-deps */
import * as React from "react";
import {Mathfield, MathfieldConfig, MathfieldElement} from "mathlive";
import "mathlive/dist/mathlive-fonts.css";
import {useEffect, useRef, useState} from "react";

export type Props = {
    latex: string;
    onChange?: (latex: string) => void;
    mathfieldConfig?: Partial<MathfieldConfig>;
    mathfieldRef?: (mathfieldElement: MathfieldElement) => void;
}

export function combineConfig(props: Props): Partial<MathfieldConfig> {
    const combinedConfiguration: Partial<MathfieldConfig> = {
        ...props.mathfieldConfig,
    };

    const {onChange} = props;

    if (onChange) {
        if (props.mathfieldConfig?.onContentDidChange) {
            const fromConfig = props.mathfieldConfig.onContentDidChange;
            combinedConfiguration.onContentDidChange = (mf: Mathfield) => {
                onChange(mf.getValue());
                fromConfig(mf);
            };
        } else {
            combinedConfiguration.onContentDidChange = (mf: Mathfield) =>
                onChange(mf.getValue());
        }
    }

    return combinedConfiguration;
}

export const MathfieldComponent = (props: Props): JSX.Element => {
    const insertElement = useRef<HTMLDivElement | null>(null)
    const [combinedConfiguration] = useState(combineConfig(props))
    const [mathfield] = useState<MathfieldElement>(new MathfieldElement(combinedConfiguration))

    // Run on initial component render
    useEffect(() => {
        if (!insertElement) return
        insertElement.current!.replaceWith(mathfield)
        mathfield.setValue(props.latex, {
            suppressChangeNotifications: true,
        })
        if (props.mathfieldRef) {
            props.mathfieldRef(mathfield)
        }
    }, [])

    useEffect(() => {
        mathfield.setValue(props.latex, {
            suppressChangeNotifications: true,
        });

    }, [props.latex])

    return <div ref={insertElement}/>
}
