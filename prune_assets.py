import os
import glob
import shutil
import sys

if len(sys.argv) < 2:
    print("Error: Pack format argument missing. Usage: python prune_assets.py <format>")
    sys.exit(1)

fmt = int(sys.argv[1])
base_dir = "build_dir/assets/minecraft"

def purge_glob(pattern):
    for path in glob.glob(os.path.join(base_dir, pattern), recursive=True):
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
            mcmeta = path + ".mcmeta"
            if os.path.exists(mcmeta):
                os.remove(mcmeta)
        elif os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)

bed_colors = ["black", "blue", "brown", "cyan", "gray", "green", "light_blue", 
              "light_gray", "lime", "magenta", "orange", "pink", "purple", "red", "white", "yellow"]

# --- SPAWN EGGS (Format <= 3 vs Format >= 4) ---
if fmt <= 3:
    purge_glob("models/item/*spawn_egg*.json")
    purge_glob("models/block/*spawn_egg*.json")
else:
    purge_glob("**/cit/spawn_egg*")
    find_color_props = glob.glob(os.path.join(base_dir, "**/color.properties"), recursive=True)
    for cp in find_color_props:
        try:
            with open(cp, "r") as f:
                lines = [l for l in f if not l.strip().startswith("egg.")]
            with open(cp, "w") as f:
                f.writelines(lines)
        except Exception:
            pass

# --- 1.21+ (Format < 88) ---
if fmt < 88:
    purge_glob("**/ctm/**/crafter*")
    purge_glob("**/ctm/**/polished_tuff*")
    purge_glob("**/ctm/**/copper/grate*")
    purge_glob("**/ctm/**/copper/chiseled*")
    purge_glob("textures/**/gui/**/crafter*")
    purge_glob("textures/**/copper_axe*")
    purge_glob("textures/**/copper_hoe*")
    purge_glob("textures/**/copper_sword*")
    purge_glob("textures/**/flow_banner_pattern*")
    purge_glob("textures/**/guster_banner_pattern*")

# --- 1.19+ (Format < 9) ---
if fmt < 9:
    purge_glob("**/ctm/**/froglights*")
    purge_glob("**/ctm/**/reinforced_deepslate*")

# --- COLORED SIGNS (< 1.14 & >= 1.18) ---
if fmt < 4 or fmt >= 8:
    purge_glob("textures/**/spruce_sign*")
    purge_glob("textures/**/birch_sign*")
    purge_glob("textures/**/jungle_sign*")
    purge_glob("textures/**/acacia_sign*")
    purge_glob("textures/**/dark_oak_sign*")

# --- 1.17+ (Format < 7) ---
if fmt < 7:
    purge_glob("**/ctm/**/chiseled_deepslate*")
    purge_glob("**/ctm/**/deepslate*")
    purge_glob("**/ctm/**/polished_deepslate*")
    purge_glob("**/ctm/**/copper*")
    purge_glob("**/ctm/**/glass/tinted_glass*")
    purge_glob("**/ctm/**/metals_and_gems/ore/copper_ore*")
    purge_glob("**/ctm/**/metals_and_gems/ore/deepslate_*")

# --- 1.16+ (Format < 6) ---
if fmt < 6:
    purge_glob("textures/**/netherite_*")
    purge_glob("textures/**/piglin_banner_pattern*")

# --- 1.15+ JAPPA RETEXTURES & BEDS (Format >= 5) ---
if fmt >= 5:
    purge_glob("textures/particle/particles.png")
    purge_glob("textures/**/cod_bucket.png")
    purge_glob("textures/**/salmon_bucket.png")
    purge_glob("textures/**/pufferfish_bucket.png")
    purge_glob("textures/**/tropical_fish_bucket.png")
    purge_glob("textures/**/beetroot_seeds.png")
    purge_glob("textures/**/seeds_beetroot.png")
    purge_glob("textures/**/sponge.png")
    purge_glob("textures/**/sponge_wet.png")
    purge_glob("textures/**/wet_sponge.png")
    purge_glob("textures/**/bed_*.png")
    for color in bed_colors:
        purge_glob(f"textures/**/{color}_bed_*.png")

# --- BONE BLOCKS (<= 1.9 and >= 1.15) ---
if fmt <= 1 or fmt >= 5:
    purge_glob("textures/**/bone_block*.png")


# --- 1.15 - 1.16+ (Format < 5) ---
if fmt < 5:
    purge_glob("**/ctm/**/beehive*")
    purge_glob("**/ctm/**/beenest*")
    purge_glob("**/ctm/**/chiseled_nether_bricks*")
    purge_glob("**/ctm/**/chiseled_polished_blackstone*")
    purge_glob("**/ctm/**/netherite_block*")
    purge_glob("**/ctm/**/polished_basalt*")
    purge_glob("**/ctm/**/polished_blackstone*")
    purge_glob("**/ctm/**/quartz_bricks*")
    purge_glob("**/ctm/**/shroomlight*")
    purge_glob("**/ctm/**/metals_and_gems/ore/nether_gold_ore*")
    purge_glob("textures/**/items/honeycomb*")
    purge_glob("textures/**/item/honeycomb*")
    purge_glob("textures/**/items/honey_bottle*")
    purge_glob("textures/**/item/honey_bottle*")
    purge_glob("textures/**/gui/**/blast_furnace*")
    purge_glob("textures/**/gui/**/smoker*")
    purge_glob("textures/**/gui/**/smithing*")
    purge_glob("textures/**/misc/enchanted_glint_item.png")
    purge_glob("textures/**/misc/enchanted_glint_armor.png")
else:
    purge_glob("textures/**/misc/enchanted_item_glint.png")

# --- STRIPPED LOGS (< 1.13) ---
if fmt < 4:
    purge_glob("textures/**/stripped_*.png")

# --- 1.14+ (Format < 4) ---
if fmt < 4:
    purge_glob("textures/particle/damage.png")
    purge_glob("textures/particle/heart.png")
    purge_glob("textures/entity/fishing_hook.png")
    purge_glob("textures/items/structure_void*")
    purge_glob("**/ctm/**/cartography_table*")
    purge_glob("**/ctm/**/loom*")
    purge_glob("textures/**/blocks/cornflower.png")
    purge_glob("textures/**/blocks/kelp*.png")
    purge_glob("textures/**/blocks/lectern_*.png")
    purge_glob("textures/**/blocks/cut_*_sandstone.png")
    purge_glob("textures/**/crossbow*")
    purge_glob("textures/**/campfire*")
    purge_glob("textures/**/lantern*")
    purge_glob("textures/**/phantom_membrane*")
    purge_glob("textures/**/sweet_berries*")
    purge_glob("textures/**/globe_banner_pattern*")
    purge_glob("textures/**/creeper_banner_pattern*")
    purge_glob("textures/**/flower_banner_pattern*")
    purge_glob("textures/**/mojang_banner_pattern*")
    purge_glob("textures/**/skull_banner_pattern*")
    purge_glob("textures/**/cod_bucket*")
    purge_glob("textures/**/salmon_bucket*")
    purge_glob("textures/**/pufferfish_bucket*")
    purge_glob("textures/**/tropical_fish_bucket*")
    purge_glob("textures/**/gui/**/cartography_table*")
    purge_glob("textures/**/gui/**/grindstone*")
    purge_glob("textures/**/gui/**/loom*")
    purge_glob("textures/**/gui/**/stonecutter*")
    purge_glob("textures/**/gui/**/nautilus*")
    purge_glob("textures/**/gui/**/recipe_book*")
    purge_glob("textures/**/gui/**/recipe_background*")
    purge_glob("textures/**/gui/**/gamemode_switcher*")
    purge_glob("textures/**/gui/**/advancements*")
    purge_glob("textures/**/oak_sign*")
    purge_glob("textures/**/black_dye*")
    purge_glob("textures/**/white_dye*")
    purge_glob("textures/**/blue_dye*")
    purge_glob("textures/**/brown_dye*")
    purge_glob("textures/**/red_dye*")
    purge_glob("textures/**/green_dye*")
    purge_glob("textures/**/yellow_dye*")
    purge_glob("textures/**/cyan_dye*")
    purge_glob("textures/**/gray_dye*")
    purge_glob("textures/**/light_blue_dye*")
    purge_glob("textures/**/light_gray_dye*")
    purge_glob("textures/**/lime_dye*")
    purge_glob("textures/**/magenta_dye*")
    purge_glob("textures/**/orange_dye*")
    purge_glob("textures/**/pink_dye*")
    purge_glob("textures/**/purple_dye*")

# --- 1.13+ FLATTENING SEPARATION (Format >= 4 vs Legacy Formats 1, 2, 3) ---
if fmt >= 4:
    legacy_blocks = [
        "brick.png", "potatoes_stage_*.png", "carrots_stage_*.png", "carrot_stage_*.png", "nether_wart_stage_*.png", "cocoa_stage_*.png",
        "endframe_*.png", "farmland_dry.png", "farmland_wet.png", "flower_allium.png",
        "flower_blue_orchid.png", "flower_dandelion.png", "flower_houstonia.png",
        "flower_oxeye_daisy.png", "flower_paeonia.png", "flower_rose.png", "flower_tulip_*.png", "flower_pot.png",
        "rail_normal.png", "rail_normal_turned.png", "rail_golden.png", "rail_golden_powered.png",
        "rail_detector.png", "rail_detector_powered.png", "rail_activator.png", "rail_activator_powered.png",
        "sandstone_normal.png", "sandstone_carved.png", "sandstone_smooth.png",
        "red_sandstone_normal.png", "red_sandstone_carved.png", "red_sandstone_smooth.png",
        "wool_colored_*.png", "melon_stem_disconnected.png", "melon_stem_connected.png",
        "pumpkin_stem_disconnected.png", "pumpkin_stem_connected.png", "mushroom_red.png", "mushroom_brown.png", "mushroom_block_skin_*.png",
        "nether_brick.png", "door_wood_*.png", "door_iron_*.png", "door_spruce_*.png", "door_birch_*.png",
        "door_jungle_*.png", "door_acacia_*.png", "door_dark_oak_*.png", "glass_black.png", "glass_red.png",
        "glass_green.png", "glass_brown.png", "glass_blue.png", "glass_purple.png", "glass_cyan.png",
        "glass_silver.png", "glass_gray.png", "glass_pink.png", "glass_lime.png", "glass_yellow.png",
        "glass_light_blue.png", "glass_magenta.png", "glass_orange.png", "glass_white.png", "glass_pane_top_*.png",
        "comparator_off.png", "furnace_front_off.png", "grass_side.png", "grass_top.png", "grass_side_snowed.png",
        "hardened_clay.png", "hardened_clay_stained_*.png", "prismarine_dark.png", "prismarine_rough.png", "leaves_oak.png",
        "leaves_oak_opaque.png", "leaves_spruce.png", "leaves_spruce_opaque.png", "leaves_birch.png",
        "leaves_birch_opaque.png", "leaves_jungle.png", "leaves_jungle_opaque.png", "leaves_acacia.png",
        "leaves_acacia_opaque.png", "leaves_big_oak.png", "leaves_big_oak_opaque.png", "slime.png",
        "redstone_lamp_off.png", "piston_top_normal.png", "anvil_base.png", "anvil_top_damaged.png", "anvil_top_damaged_0.png", "anvil_top_damaged_1.png", "anvil_top_damaged_2.png",
        "web.png", "wheat_stage_*.png", "stone_slab_top.png", "stone_slab_side.png",
        "stonebrick.png", "stonebrick_mossy.png", "stonebrick_cracked.png", "stonebrick_carved.png",
        "cobblestone_mossy.png", "sapling_*.png", "redstone_torch_on.png", "redstone_torch_off.png",
        "stone_andesite*.png", "stone_diorite*.png", "stone_granite*.png",
        "log_oak*.png", "log_spruce*.png", "log_birch*.png", "log_jungle*.png", "log_acacia*.png", "log_big_oak*.png", "log_dark_oak*.png",
        "planks_*.png", "tallgrass.png", "double_plant_*.png", "trip_wire.png", "trip_wire_source.png", "deadbush.png", "trapdoor.png",
        "torch_on.png", "item_frame.png", "reeds.png", "sponge_wet.png"
    ]
    for lb in legacy_blocks:
        purge_glob("textures/blocks/" + lb)

    purge_glob("textures/item/potato_poisonous.png")
    purge_glob("textures/item/potato_baked.png")
    purge_glob("textures/**/pumpkin_face_off.png")
    purge_glob("textures/**/pumpkin_face_on.png")
    purge_glob("textures/item/fishing_rod_uncast.png")
    purge_glob("textures/item/fireball.png")
    purge_glob("textures/item/fireworks.png")
    purge_glob("textures/item/wooden_armorstand.png")
    purge_glob("textures/item/wood_sword.png")
    purge_glob("textures/item/wood_pickaxe.png")
    purge_glob("textures/item/wood_axe.png")
    purge_glob("textures/item/wood_shovel.png")
    purge_glob("textures/item/wood_hoe.png")
    purge_glob("textures/item/gold_helmet.png")
    purge_glob("textures/item/gold_chestplate.png")
    purge_glob("textures/item/gold_leggings.png")
    purge_glob("textures/item/gold_boots.png")
    purge_glob("textures/item/gold_sword.png")
    purge_glob("textures/item/gold_pickaxe.png")
    purge_glob("textures/item/gold_axe.png")
    purge_glob("textures/item/gold_shovel.png")
    purge_glob("textures/item/gold_hoe.png")
    purge_glob("textures/item/beef_raw.png")
    purge_glob("textures/item/beef_cooked.png")
    purge_glob("textures/item/chicken_raw.png")
    purge_glob("textures/item/chicken_cooked.png")
    purge_glob("textures/item/porkchop_raw.png")
    purge_glob("textures/item/porkchop_cooked.png")
    purge_glob("textures/item/mutton_raw.png")
    purge_glob("textures/item/mutton_cooked.png")
    purge_glob("textures/item/rabbit_raw.png")
    purge_glob("textures/item/rabbit_cooked.png")
    purge_glob("textures/item/fish_cod_raw.png")
    purge_glob("textures/item/fish_cod_cooked.png")
    purge_glob("textures/item/fish_salmon_raw.png")
    purge_glob("textures/item/fish_salmon_cooked.png")
    purge_glob("textures/item/fish_pufferfish_raw.png")
    purge_glob("textures/item/fish_clownfish_raw.png")
    purge_glob("textures/item/melon.png")
    purge_glob("textures/item/melon_speckled.png")
    purge_glob("textures/item/apple_golden.png")
    purge_glob("textures/item/carrot_golden.png")
    purge_glob("textures/item/minecart_normal.png")
    purge_glob("textures/item/minecart_*.png")
    purge_glob("textures/item/door_*.png")
    purge_glob("textures/item/dye_powder_*.png")
    purge_glob("textures/item/record_*.png")
    purge_glob("textures/item/seeds_*.png")
    purge_glob("textures/item/potion_bottle_*.png")
    purge_glob("textures/item/empty_armor_slot_*.png")
    purge_glob("textures/item/fireworks_charge*.png")
    purge_glob("textures/item/redstone_dust.png")
    purge_glob("textures/item/reeds.png")
    purge_glob("textures/item/slimeball.png")
    purge_glob("textures/item/netherbrick.png")
    purge_glob("textures/item/sign.png")
    purge_glob("textures/item/bucket_empty.png")
    purge_glob("textures/item/bucket_water.png")
    purge_glob("textures/item/bucket_lava.png")
    purge_glob("textures/item/bucket_milk.png")
    purge_glob("textures/item/book_normal.png")
    purge_glob("textures/item/book_enchanted.png")
    purge_glob("textures/item/book_writable.png")
    purge_glob("textures/item/book_written.png")
    purge_glob("textures/item/map_empty.png")
    purge_glob("textures/item/map_filled.png")
    purge_glob("textures/item/totem.png")
else:
    modern_blocks = [
        "bricks.png", "potatoes_stage[0-9].png", "carrots_stage[0-9].png", "nether_wart_stage[0-9].png", "cocoa_stage[0-9].png",
        "end_portal_frame_*.png", "farmland.png", "farmland_moist.png", "allium.png", "blue_orchid.png",
        "dandelion.png", "azure_bluet.png", "oxeye_daisy.png", "peony_*.png", "poppy.png", "*_tulip.png", "potted_*.png",
        "rail.png", "powered_rail.png", "powered_rail_on.png", "detector_rail.png", "detector_rail_on.png",
        "activator_rail.png", "activator_rail_on.png", "sandstone.png", "chiseled_sandstone.png", "cut_sandstone.png",
        "red_sandstone.png", "chiseled_red_sandstone.png", "cut_red_sandstone.png",
        "*_wool.png", "melon_stem.png", "attached_melon_stem.png",
        "pumpkin_stem.png", "attached_pumpkin_stem.png", "red_mushroom_block.png", "brown_mushroom_block.png", "mushroom_stem.png", "nether_bricks.png",
        "oak_door_*.png", "iron_door_*.png", "spruce_door_*.png", "birch_door_*.png", "jungle_door_*.png",
        "acacia_door_*.png", "dark_oak_door_*.png", "*_stained_glass.png", "*_stained_glass_pane*.png",
        "comparator.png", "furnace_front.png", "grass_block_*.png", "terracotta.png", "*_terracotta.png", "dark_prismarine.png", "prismarine.png",
        "oak_leaves.png", "spruce_leaves.png", "birch_leaves.png", "jungle_leaves.png",
        "acacia_leaves.png", "dark_oak_leaves.png", "slime_block.png", "redstone_lamp.png", "piston_top.png",
        "anvil.png", "anvil_top.png", "chipped_anvil_top.png", "damaged_anvil_top.png", "anvil_top_damaged.png",
        "cobweb.png", "wheat_stage[0-7].png", "smooth_stone_slab_*.png",
        "stone_bricks.png", "mossy_stone_bricks.png", "cracked_stone_bricks.png", "chiseled_stone_bricks.png",
        "mossy_cobblestone.png", "*_sapling.png", "redstone_torch.png", "unlit_redstone_torch.png",
        "andesite.png", "diorite.png", "granite.png", "polished_andesite.png", "polished_diorite.png", "polished_granite.png",
        "oak_log*.png", "spruce_log*.png", "birch_log*.png", "jungle_log*.png", "acacia_log*.png", "dark_oak_log*.png",
        "*_planks.png", "tall_grass*.png", "large_fern_*.png", "lilac_*.png", "peony_*.png", "rose_bush_*.png", "sunflower_*.png",
        "tripwire.png", "tripwire_hook.png", "dead_bush.png", "oak_trapdoor.png", "torch.png", "itemframe_background.png",
        "sugar_cane.png", "wet_sponge.png"
    ]
    for mb in modern_blocks:
        purge_glob("textures/blocks/" + mb)

    # Special handling for legacy items/entities renamed in modern
    purge_glob("textures/items/map.png")
    purge_glob("textures/items/filled_map.png")
    purge_glob("textures/items/filled_map_markings.png")
    purge_glob("textures/items/poisonous_potato.png")
    purge_glob("textures/items/baked_potato.png")
    purge_glob("textures/**/carved_pumpkin.png")
    purge_glob("textures/**/jack_o_lantern.png")
    purge_glob("textures/items/fishing_rod.png")
    purge_glob("textures/items/fire_charge.png")
    purge_glob("textures/items/firework_rocket.png")
    purge_glob("textures/items/armor_stand.png")
    purge_glob("textures/items/wooden_sword.png")
    purge_glob("textures/items/wooden_pickaxe.png")
    purge_glob("textures/items/wooden_axe.png")
    purge_glob("textures/items/wooden_shovel.png")
    purge_glob("textures/items/wooden_hoe.png")
    purge_glob("textures/items/golden_helmet.png")
    purge_glob("textures/items/golden_chestplate.png")
    purge_glob("textures/items/golden_leggings.png")
    purge_glob("textures/items/golden_boots.png")
    purge_glob("textures/items/golden_sword.png")
    purge_glob("textures/items/golden_pickaxe.png")
    purge_glob("textures/items/golden_axe.png")
    purge_glob("textures/items/golden_shovel.png")
    purge_glob("textures/items/golden_hoe.png")
    purge_glob("textures/items/beef.png")
    purge_glob("textures/items/cooked_beef.png")
    purge_glob("textures/items/chicken.png")
    purge_glob("textures/items/cooked_chicken.png")
    purge_glob("textures/items/porkchop.png")
    purge_glob("textures/items/cooked_porkchop.png")
    purge_glob("textures/items/mutton.png")
    purge_glob("textures/items/cooked_mutton.png")
    purge_glob("textures/items/rabbit.png")
    purge_glob("textures/items/cooked_rabbit.png")
    purge_glob("textures/items/cod.png")
    purge_glob("textures/items/cooked_cod.png")
    purge_glob("textures/items/salmon.png")
    purge_glob("textures/items/cooked_salmon.png")
    purge_glob("textures/items/pufferfish.png")
    purge_glob("textures/items/tropical_fish.png")
    purge_glob("textures/items/melon_slice.png")
    purge_glob("textures/items/glistering_melon_slice.png")
    purge_glob("textures/items/golden_apple.png")
    purge_glob("textures/items/golden_carrot.png")
    purge_glob("textures/items/sugar_cane.png")
    purge_glob("textures/items/slime_ball.png")
    purge_glob("textures/items/nether_brick.png")
    purge_glob("textures/items/totem_of_undying.png")
    purge_glob("textures/items/book.png")
    purge_glob("textures/items/enchanted_book.png")
    purge_glob("textures/items/writable_book.png")
    purge_glob("textures/items/written_book.png")
    purge_glob("textures/items/potion.png")
    purge_glob("textures/items/glass_bottle.png")
    purge_glob("textures/items/bucket.png")
    purge_glob("textures/items/water_bucket.png")
    purge_glob("textures/items/lava_bucket.png")
    purge_glob("textures/items/milk_bucket.png")
    purge_glob("textures/items/redstone.png")
    purge_glob("textures/items/bone_meal.png")
    purge_glob("textures/items/cocoa_beans.png")
    purge_glob("textures/items/lapis_lazuli.png")
    purge_glob("textures/items/ink_sac.png")
    purge_glob("textures/items/wheat_seeds.png")
    purge_glob("textures/items/melon_seeds.png")
    purge_glob("textures/items/pumpkin_seeds.png")
    purge_glob("textures/items/music_disc_*.png")
    purge_glob("textures/items/minecart.png")
    purge_glob("textures/items/chest_minecart.png")
    purge_glob("textures/items/furnace_minecart.png")
    purge_glob("textures/items/tnt_minecart.png")
    purge_glob("textures/items/hopper_minecart.png")
    purge_glob("textures/items/command_block_minecart.png")
    purge_glob("textures/items/oak_door.png")
    purge_glob("textures/items/spruce_door.png")
    purge_glob("textures/items/birch_door.png")
    purge_glob("textures/items/jungle_door.png")
    purge_glob("textures/items/acacia_door.png")
    purge_glob("textures/items/dark_oak_door.png")
    purge_glob("textures/items/iron_door.png")

# --- COLORED BEDS UNDER 1.12 ---
if fmt < 3:
    for color in bed_colors:
        purge_glob(f"textures/**/{color}_bed_*.png")

# --- 1.11 - 1.12+ (Format < 3) ---
if fmt < 3:
    purge_glob("textures/**/gui/**/shulker_box*")
    purge_glob("textures/**/shulker_shell*")
    purge_glob("textures/**/iron_nugget*")
    purge_glob("textures/**/totem*")
    purge_glob("textures/**/knowledge_book*")

    # --- RED NETHER BRICKS (< 1.10) ---
if fmt <= 2:
    purge_glob("textures/**/red_nether_bricks.png")

# --- CLOCK & COMPASS HANDLING ---
if fmt >= 2:
    purge_glob("textures/items/clock.png")
    purge_glob("textures/items/clock.png.mcmeta")
    purge_glob("textures/items/compass.png")
    purge_glob("textures/items/compass.png.mcmeta")

# --- PURPUR BLOCKS (< 1.9) ---
if fmt < 2:
    purge_glob("textures/**/purpur_*.png")
    purge_glob("**/ctm/**/purpur*")
    purge_glob("models/block/purpur_pillar*.json")
    purge_glob("blockstates/purpur_pillar.json")

# --- 1.9 - 1.10+ (Format == 1 / 1.8.9 Base) ---
if fmt == 1:
    purge_glob("**/ctm/**/bone*")
    purge_glob("models/block/*command_block*.json")
    purge_glob("models/item/*command_block*.json")
    purge_glob("blockstates/*command_block*.json")
    purge_glob("textures/**/blocks/magma.png")
    purge_glob("textures/**/blocks/nether_wart_block.png")
    purge_glob("textures/**/blocks/beetroots_stage*.png")
    purge_glob("textures/**/blocks/chorus_*.png")
    purge_glob("textures/**/blocks/end_rod.png")
    purge_glob("textures/**/blocks/frosted_ice_*.png")
    purge_glob("textures/**/blocks/end_bricks.png")
    purge_glob("textures/**/blocks/*_trapdoor.png")
    purge_glob("textures/**/blocks/chain_command_block.*")
    purge_glob("textures/**/blocks/repeating_command_block.*")
    purge_glob("textures/items/*_boat.png")
    purge_glob("textures/items/clock_*.png")
    purge_glob("textures/items/compass_*.png")
    purge_glob("textures/items/spectral_arrow*")
    purge_glob("textures/items/dragon_breath*")
    purge_glob("textures/items/splash_potion*")
    purge_glob("textures/items/lingering_potion*")
    purge_glob("textures/items/elytra*")
    purge_glob("textures/items/chorus_fruit*")
    purge_glob("textures/items/popped_chorus_fruit*")
    purge_glob("textures/items/beetroot*")
    purge_glob("textures/items/end_crystal*")
    purge_glob("textures/items/empty_armor_slot_shield*")

    # Bed textures
    for color in bed_colors:
        purge_glob(f"textures/**/blocks/{color}_bed_*")

    # Modern blocks in 1.8.9
    redundant_blocks_1_8 = [
        "blocks/carrots_stage[0-7].png", "blocks/cocoa_stage[0-7].png",
        "blocks/nether_wart_stage[0-7].png", "blocks/oak_planks.png", "blocks/birch_planks.png",
        "blocks/spruce_planks.png", "blocks/jungle_planks.png", "blocks/acacia_planks.png",
        "blocks/dark_oak_planks.png", "blocks/oak_log*.png", "blocks/birch_log*.png",
        "blocks/spruce_log*.png", "blocks/jungle_log*.png", "blocks/acacia_log*.png",
        "blocks/dark_oak_log*.png", "blocks/grass_block_*.png",
        "blocks/end_stone_bricks.png", "blocks/short_grass.png", "blocks/allium.png",
        "blocks/azure_bluet.png", "blocks/blue_orchid.png", "blocks/dandelion.png",
        "blocks/dead_bush.png", "blocks/fire_0.png", "blocks/fire_1.png",
        "blocks/furnace_front.png", "blocks/dispenser_front.png", "blocks/dropper_front.png",
        "blocks/attached_*_stem.png", "blocks/melon_stem.png", "blocks/pumpkin_stem.png",
        "blocks/nether_bricks.png", "blocks/nether_portal.png", "blocks/iron_door_*.png",
        "blocks/oak_door_*.png", "blocks/andesite.png", "blocks/diorite.png", "blocks/granite.png"
    ]
    for pat in redundant_blocks_1_8:
        purge_glob("textures/" + pat)

# Clean up empty directories
for root, dirs, files in os.walk(base_dir, topdown=False):
    for d in dirs:
        dir_path = os.path.join(root, d)
        if not os.listdir(dir_path):
            try:
                os.rmdir(dir_path)
            except OSError:
                pass

print(f"Asset pruning complete for Format {fmt}.")