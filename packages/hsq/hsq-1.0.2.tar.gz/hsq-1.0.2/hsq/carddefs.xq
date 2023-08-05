xquery version "3.1";

declare variable $enums := doc("enums.xml")/Enums;

declare variable $unimpl := doc("unimpl.xml")/Unimplemented;

declare function local:reverse-map($enum as xs:string, $value as xs:string) as xs:string {
    $enums/Enum[@name=$enum]/Member[@value=$value][1]/@name/string()
};

declare function local:tag-fixup($tag as element()) as element() {
    element {node-name($tag)} {
        $tag/@* except $tag/@value,

        if (not($tag/@name))
            then attribute name {local:reverse-map("GameTag", $tag/@enumID)}
            else (),

        attribute value {
            switch ($tag/@type)
                case "String"    return $tag/string()
                case "LocString" return $tag/enUS/string()
                case "Int"       return xs:integer($tag/@value)
                default          return $tag/@value
        }
    }
};

declare function local:tags-to-attributes($tags as element()*) as attribute()* {
        (: Process regular tags :)
        for $tag in $tags
        group by $name := $tag/@name
        let $tag := $tag[1]
        (: Filter out false booleans so we can use @Attribute as a shorthand :)
        where $tag/@type != "Bool" or $tag/@value = "1"
        where $name != "CardTextInHand"
        let $value := switch ($name)
            case "Class" return local:reverse-map("CardClass", $tag/@value)
            default return if ($enums/Enum[@name=$name])
                then local:reverse-map($name, $tag/@value)
                else $tag/@value
        let $name := replace($name, "^Card", "")
        return attribute {replace($name, "\s+", "")} {$value}
};

declare function local:transform-card($n as element()) as element() {
    let $text := parse-xml-fragment($n/Tag[@name="CardTextInHand"]/enUS)
    let $tags := $n/Tag ! local:tag-fixup(.)

    return element Card {
        $n/@*,

        local:tags-to-attributes($tags),

        (: "Elusive" has no tag :)
        if ($tags[@name="CANT_BE_TARGETED_BY_ABILITIES"][@value=1]
        and $tags[@name="CANT_BE_TARGETED_BY_HERO_POWERS"][@value=1])
            then attribute {"Elusive"} {1}
            else (),

        if ($unimpl/ID=$n/@CardID)
            then attribute {"FireplaceMissing"} {1}
            else (),

        (: Text is special :)
        <Text>{$text}</Text>,

        element RefersTo {
            local:tags-to-attributes($n/ReferencedTag ! local:tag-fixup(.))
        },

        $n/* except $n/Tag
    }
};

declare function local:generate-card-xml($cards as node()) as element() {
    <Cards>
    {
        $cards/CardDefs/Entity ! local:transform-card(.)
    }
    </Cards>
};

local:generate-card-xml(.)
