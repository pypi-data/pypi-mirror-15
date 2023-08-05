xquery version "3.1";

module namespace hs = "https://kellett.im/xq/hs";

declare %private variable $hs:cards := doc("cards.xml")/Cards/Card;

declare function hs:search($x) { $hs:cards[(@*, Text)[contains(lower-case(.), lower-case($x))]] };

declare function hs:cards()    { $hs:cards[@Collectible][@Type!="HERO"] };
declare function hs:minions()  { $hs:cards[@Collectible][@Type="MINION"] };
declare function hs:spells()   { $hs:cards[@Collectible][@Type="SPELL"] };
declare function hs:weapons()  { $hs:cards[@Collectible][@Type="WEAPON"] };

declare function hs:classes()  { distinct-values($hs:cards[@Collectible]/@Class/string()) };

declare function hs:all-cards() { $hs:cards };
declare function hs:class-cards($class as xs:string) {
    $hs:cards[@Collectible][not(@Class) or @Class=$class]
};
declare function hs:class-only($class as xs:string) {
    $hs:cards[@Collectible][@Class=$class]
};

declare %private variable $hs:groups := (
    <Group name="Kraken">
        <Set>BRM</Set>
        <Set>TGT</Set>
        <Set>LOE</Set>
        <Set>OG</Set>
    </Group>
);

declare %private variable $hs:standard_year := "Kraken";

declare function hs:set($s as xs:string) { $hs:cards[@Set=$s] };

declare function hs:standard() { hs:standard($hs:standard_year) };

declare function hs:standard($year as xs:string) {
    let $standard := $hs:groups[@name=$year]
    return if (not($standard))
        then error(xs:QName("hs:e1"), "not a standard year: " || $year)
        else
            let $sets := (<Set>CORE</Set>, <Set>EXPERT1</Set>) union $hs:groups[@name=$year]/Set
            return hs:cards()[let $x := @Set return $sets[.=$x]]
};

declare %private function hs:sort-by($cards as element(Card)*, $attr as xs:string) {
    let $qn := xs:QName($attr)
    for $card in $cards
    let $atn := $card/@*[node-name(.) = $qn]
    where ($atn)
    group by $at := xs:integer($atn)
    order by $at ascending
    return <Cards>{$card}</Cards>
};

declare function hs:min($cards as element(Card)*, $attr as xs:string) {
    hs:sort-by($cards, $attr)[1]/*
};

declare function hs:max($cards as element(Card)*, $attr as xs:string) {
    hs:sort-by($cards, $attr)[last()]/*
};
