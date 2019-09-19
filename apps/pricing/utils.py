from apps.logistics.models import ExpressFeeGroup
from apps.pricing.models import Pricing, TieredPricing, StepPrice
from apps.user.models import AgentGroup
from apps.user.utils import create_agent_group


def create_pricing(spec,
                   is_free_shipping=True,
                   express_fee_group_id=None,
                   currency='',
                   step_one_min=0,
                   step_one_max=0,
                   price_one=0,
                   step_two_min=0,
                   step_two_max=0,
                   price_two=0,
                   step_three_min=0,
                   step_three_max=0,
                   price_three=0,
                   retail_price=0,
                   suggest_retail_price=0):
    pricing = Pricing()
    pricing.spec = spec
    if is_free_shipping:
        pricing.is_free_shipping = True
        pricing.express_fee_group = None
    else:
        pricing.is_free_shipping = False
        express_fee_group_set = ExpressFeeGroup.objects.filter(id__extra=int(express_fee_group_id))
        if express_fee_group_set:
            pricing.express_fee_group = express_fee_group_set[0]
        else:
            return '快递费模板编号不正确'
    pricing.currency = currency
    pricing.cost = 0
    pricing.retail_price = retail_price
    pricing.suggested_retail_price = suggest_retail_price
    pricing.is_general = True
    if step_one_min == 0 and step_one_max == 0:
        pricing.has_tiered_pricing = False
        pricing.wholesale_price = price_one
    else:
        pricing.has_tiered_pricing = True
        pricing.wholesale_price = 0
    agent_group_set = AgentGroup.objects.filter(supplier=spec.product.creator, name='默认')
    if agent_group_set:
        pricing.agent_group = agent_group_set[0]
    else:
        pricing.agent_group = create_agent_group(spec.product.creator, '默认')
    pricing.save()

    # ***创建该规格的定价***
    if pricing.has_tiered_pricing:
        tiered_pricing = create_tiered_pricing(pricing,
                                               step_one_min=step_one_min,
                                               step_one_max=step_one_max,
                                               price_one=price_one,
                                               step_two_min=step_two_min,
                                               step_two_max=step_two_max,
                                               price_two=price_two,
                                               step_three_min=step_three_min,
                                               step_three_max=step_three_max,
                                               price_three=price_three)
        if type(tiered_pricing) == str:
            return tiered_pricing

    return pricing


def create_tiered_pricing(pricing,
                          step_one_min=0,
                          step_one_max=0,
                          price_one=0,
                          step_two_min=0,
                          step_two_max=0,
                          price_two=0,
                          step_three_min=0,
                          step_three_max=0,
                          price_three=0, ):
    tiered_pricing = TieredPricing()
    tiered_pricing.pricing = pricing
    tiered_pricing.save()
    step_one = create_step_price(
        tiered_pricing, min_quantity=step_one_min, max_quantity=step_one_max, price=price_one)
    if step_one is not None:
        if step_one.max_quantity > 0:
            step_two = create_step_price(
                tiered_pricing, min_quantity=step_two_min, max_quantity=step_two_max,
                pre_max_quantity=step_one_max, price=price_two)
            if step_two is not None:
                if step_two.max_quantity > 0:
                    step_three = create_step_price(
                        tiered_pricing, min_quantity=step_three_min, max_quantity=step_three_max,
                        pre_max_quantity=step_two_max, price=price_three)
                    if step_three is not None:
                        return tiered_pricing
                    else:
                        return '阶梯3，数量区间有重叠或价格设置有误'
                else:
                    return tiered_pricing
            else:
                return '阶梯2，数量区间有重叠或价格设置有误'
        else:
            return tiered_pricing
    else:
        return '阶梯1，数量区间有重叠或价格设置有误'


def create_step_price(tiered_pricing, min_quantity=0, max_quantity=0, pre_max_quantity=0, price=0):
    step_price = StepPrice()
    step_price.tiered_pricing = tiered_pricing
    step_price.min_quantity = min_quantity
    step_price.max_quantity = max_quantity
    step_price.price = price
    if pre_max_quantity > 0:
        if pre_max_quantity + 1 == min_quantity and (max_quantity == 0 or min_quantity <= max_quantity) and price > 0:
            step_price.save()
            return step_price
        else:
            return None
    else:
        if 0 < min_quantity <= max_quantity and price > 0:
            step_price.save()
            return step_price
        else:
            return None
