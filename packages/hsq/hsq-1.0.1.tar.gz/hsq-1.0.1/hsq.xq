xquery version "3.1";

module namespace hsq = "https://kellett.im/xq/hsq";

import module namespace hs = "https://kellett.im/xq/hs" at "hs.xq";

declare function hsq:evaluate($input as xs:string) {
    let $result := xquery:eval($input, map {'': hs:cards()}, map {'permission': 'none'})

    return typeswitch($result)
        case empty-sequence() return
            <Results type="empty"/>

        case element(Card)+ return
            <Results type="cards">{$result}</Results>

        case attribute()+ return
            <Results type="list"> {
                $result ! <Element>{./string()}</Element>
            } </Results>

        case xs:anyAtomicType+ return
            <Results type="list"> {
                $result ! <Element>{.}</Element>
            } </Results>

        case array(*) return
            <Results type="list"> {
                for $k in 1 to array:size($result)
                return <Element>{$result($k)}</Element>
            } </Results>

        case array(*)+ return
            <Results type="table"> {
                $result !
                    <Row> {
                        for $k in 1 to array:size(.)
                        return <Cell>{.($k)}</Cell>
                    } </Row>
            } </Results>

        default return
            <Results type="unknown">{$result}</Results>
};
