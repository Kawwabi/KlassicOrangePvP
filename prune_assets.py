import os
import glob
import shutil
import sys

if len(sys.argv) < 2:
    print("Error: Pack format argument missing. Usage: python prune_assets.py <format>")
    sys.exit(1)

fmt = int(sys.argv[1])
base_dir = "build_dir/assets/minecraft"

# Because of the Bash script's pre-processing, we know exactly which folder names are used.
blocks_dir = "textures/block" if fmt >= 4 else "textures/blocks"
items_dir = "textures/item" if fmt >= 4 else "textures/items"

def purge_glob(pattern):
    for path in glob.glob(os.path.join(base_dir, pattern), recursive=True):
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
            # Automatically catches and deletes the associated .mcmeta file
            mcmeta = path + ".mcmeta"
            if os.path.exists(mcmeta):
                os.remove(mcmeta)
        elif os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)

bed_colors = ["black", "blue", "brown", "cyan", "gray", "green", "light_blue", 
              "light_gray", "lime", "magenta", "orange", "pink", "purple", "red", "white", "yellow"]

# =========================================================================
# VERSION WINDOWS
# Format: "file_pattern": (min_format, max_format)
# Use 'None' as the max_format to indicate "this version and above" (e.g. 88+)
# Banners and Spawn Eggs are excluded to allow for backporting.
# =========================================================================
version_windows = {
    # --- TEXTURE REPLACEMENTS ---
    f"{blocks_dir}/*_glazed_terracotta.png": (3, 14), 
    "textures/entity/zombie_pigman.png": (1, 4),      
    
    # --- 1.21+ CONTENT ---
    "**/crafter*": (88, None),
    "**/polished_tuff*": (88, None),
    "**/copper/grate*": (88, None),
    "**/copper/chiseled*": (88, None),
    f"{items_dir}/copper_axe*": (88, None),
    f"{items_dir}/copper_hoe*": (88, None),
    f"{items_dir}/copper_sword*": (88, None),
    "**/environment/celestial*": (75, None),
    
    # --- 1.19.4+ GLINTS ---
    "**/enchanted_glint_entity.png": (13, None),
    "**/enchanted_glint_item.png": (13, None),
    "**/enchanted_glint_armor.png": (13, None),
    "**/enchanted_item_glint.png": (1, 12),

    # --- 1.19+ CONTENT ---
    "**/froglights*": (9, None),
    "**/reinforced_deepslate*": (9, None),
    
    # --- 1.17+ CONTENT ---
    "**/chiseled_deepslate*": (7, None),
    "**/deepslate*": (7, None),
    "**/polished_deepslate*": (7, None),
    "**/glass/tinted_glass*": (7, None),
    "**/metals_and_gems/copper*": (7, None),
    "**/metals_and_gems/ore/deepslate_*": (7, None),
    "**/metals_and_gems/ore/copper_ore*": (7, None),
    f"{items_dir}/amethyst_shard.png": (7, None),
    
    # --- 1.16+ CONTENT ---
    "textures/**/netherite_*": (5, None),
    "textures/**/zombified_piglin.png": (5, None),
    "**/chiseled_nether_bricks*": (5, None),
    "**/chiseled_polished_blackstone*": (5, None),
    "**/netherite_block*": (5, None),
    "**/polished_basalt*": (5, None),
    "**/polished_blackstone*": (5, None),
    "**/quartz_bricks*": (5, None),
    "**/shroomlight*": (5, None),
    "**/ore/nether_gold_ore*": (5, None),
    
    # --- 1.15+ CONTENT ---
    "**/ctm/default/bee*": (5, None),
    "**/honeycomb*": (5, None),
    
    # --- 1.14+ CONTENT (AND PARTICLES) ---
    "**/ctm/default/cartography_table*": (4, None),
    "**/ctm/default/loom*": (4, None),
    "**/polished/smooth_stone*": (4, None),
    f"{blocks_dir}/cornflower.png": (4, None),
    f"{blocks_dir}/kelp*.png": (4, None),
    f"{blocks_dir}/lectern_*.png": (4, None),
    f"{blocks_dir}/cut_*_sandstone.png": (4, None),
    f"{items_dir}/crossbow*": (4, None),
    f"{items_dir}/campfire*": (4, None),
    f"{items_dir}/lantern*": (4, None),
    f"{items_dir}/phantom_membrane*": (4, None),
    "textures/particle/damage.png": (4, None),
    "textures/particle/heart.png": (4, None),
    "textures/particle/particles.png": (1, 3), 
    
    # --- 1.13+ CONTENT ---
    f"{blocks_dir}/stripped_*.png": (4, None),
    
    # --- 1.9 & 1.10+ CONTENT ---
    f"{blocks_dir}/purpur_*.png": (2, None),
    "**/ctm/default/purpur*": (2, None),
    f"{blocks_dir}/bone_block*.png": (2, None),
    "**/ctm/default/bone_ends*": (2, None),
    f"{blocks_dir}/end_rod.png": (2, None),
    f"{blocks_dir}/chorus_*.png": (2, None),
    f"{items_dir}/elytra*": (2, None),
}

for pattern, (min_fmt, max_fmt) in version_windows.items():
    if fmt < min_fmt or (max_fmt is not None and fmt > max_fmt):
        purge_glob(pattern)

# =========================================================================
# CLOCK & COMPASS HANDLING
# =========================================================================
if fmt == 1:
    purge_glob(f"{items_dir}/clock_*.png")
    purge_glob(f"{items_dir}/compass_*.png")
else:
    purge_glob(f"{items_dir}/clock.png")
    purge_glob(f"{items_dir}/compass.png")

# =========================================================================
# SPAWN EGGS & OPTIFINE CIT
# =========================================================================
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

# =========================================================================
# TERRACOTTA VS HARDENED CLAY BLOCK TEXTURE PRUNING
# =========================================================================
if fmt >= 4:
    purge_glob(f"{blocks_dir}/hardened_clay.png")
    purge_glob(f"{blocks_dir}/hardened_clay_stained_*.png")
else:
    purge_glob(f"{blocks_dir}/terracotta.png")
    purge_glob(f"{blocks_dir}/*_terracotta.png")

# =========================================================================
# ARMOR PRUNING FOR 1.14+ (Targeting specific materials avoids breaking empty slots)
# =========================================================================
if fmt >= 4:
    purge_glob("textures/models/armor/*.png")
    purge_glob("textures/entity/horse/armor/*.png")
    
    armor_materials = ["leather", "chainmail", "iron", "gold", "golden", "diamond", "netherite", "turtle"]
    for mat in armor_materials:
        for piece in ["helmet", "chestplate", "leggings", "boots"]:
            purge_glob(f"{items_dir}/{mat}_{piece}.png")
        purge_glob(f"{items_dir}/{mat}_horse_armor.png")

# =========================================================================
# LEGACY VS MODERN FLATTENING SEPARATIONS & RENAMES
# =========================================================================
if fmt < 4 or fmt > 8:
    # Deletes colored signs, preserves them for 1.14-1.18 specifically
    purge_glob(f"{blocks_dir}/*_sign*.png") 

if fmt < 4:
    modern_dyes = ["black", "white", "blue", "brown", "red", "green", "yellow", "cyan", "gray", "light_blue", "light_gray", "lime", "magenta", "orange", "pink", "purple"]
    for dye in modern_dyes:
        purge_glob(f"{items_dir}/{dye}_dye*")

if fmt >= 4:
    # FORMAT 4+ / 1.13+ - DELETE LEGACY FILES
    legacy_blocks = [
        "brick.png", "potatoes_stage_*.png", "carrots_stage_*.png", "carrot_stage_*.png", "nether_wart_stage_*.png", "cocoa_stage_*.png",
        "endframe_*.png", "farmland_dry.png", "farmland_wet.png", "flower_allium.png", "flower_blue_orchid.png", "flower_dandelion.png", 
        "flower_houstonia.png", "flower_oxeye_daisy.png", "flower_pot.png", "flower_rose.png", "flower_tulip_*.png", "rail_normal.png", 
        "rail_normal_turned.png", "rail_golden.png", "rail_golden_powered.png", "rail_detector.png", "rail_detector_powered.png", 
        "rail_activator.png", "rail_activator_powered.png", "sandstone_normal.png", "sandstone_carved.png", "sandstone_smooth.png",
        "red_sandstone_normal.png", "red_sandstone_carved.png", "red_sandstone_smooth.png", "wool_colored_*.png", "melon_stem_disconnected.png", 
        "melon_stem_connected.png", "pumpkin_stem_disconnected.png", "pumpkin_stem_connected.png", "mushroom_red.png", "mushroom_brown.png", 
        "mushroom_block_skin_*.png", "nether_brick.png", "door_wood_*.png", "door_iron_*.png", "door_spruce_*.png", "door_birch_*.png",
        "door_jungle_*.png", "door_acacia_*.png", "door_dark_oak_*.png", "glass_*.png", "glass_pane_top_*.png", "comparator_off.png", 
        "furnace_front_off.png", "grass_side.png", "grass_top.png", "grass_side_snowed.png", "hardened_clay.png", "hardened_clay_stained_*.png", 
        "prismarine_dark.png", "prismarine_rough.png", "leaves_oak.png", "leaves_oak_opaque.png", "leaves_spruce.png", "leaves_spruce_opaque.png", 
        "leaves_birch.png", "leaves_birch_opaque.png", "leaves_jungle.png", "leaves_jungle_opaque.png", "leaves_acacia.png", "leaves_acacia_opaque.png", 
        "leaves_big_oak.png", "leaves_big_oak_opaque.png", "slime.png", "redstone_lamp_off.png", "piston_top_normal.png", "anvil_base.png", 
        "anvil_top_damaged_*.png", "web.png", "wheat_stage_*.png", "stone_slab_top.png", "stone_slab_side.png", "stonebrick.png", "stonebrick_mossy.png", 
        "stonebrick_cracked.png", "stonebrick_carved.png", "cobblestone_mossy.png", "sapling_*.png", "redstone_torch_on.png", "redstone_torch_off.png",
        "stone_andesite*.png", "stone_diorite*.png", "stone_granite*.png", "log_*.png", "planks_*.png", "tallgrass.png", "double_plant_*.png", 
        "trip_wire.png", "trip_wire_source.png", "deadbush.png", "trapdoor.png", "torch_on.png", "item_frame.png", "reeds.png", "sponge_wet.png",
        "dropper_front_vertical.png", "dropper_front_horizontal.png", "dispenser_front_vertical.png", "dispenser_front_horizontal.png",
        "noteblock.png", "ice_packed.png", "quartz_ore.png", "quartz_block_lines.png", "quartz_block_lines_top.png"
    ]
    for lb in legacy_blocks:
        purge_glob(f"{blocks_dir}/{lb}")

    legacy_items = [
        "potato_poisonous.png", "potato_baked.png", "fishing_rod_uncast.png", "fireball.png", "fireworks.png", "wooden_armorstand.png", 
        "wood_sword.png", "wood_pickaxe.png", "wood_axe.png", "wood_shovel.png", "wood_hoe.png", "gold_helmet.png", "gold_chestplate.png", 
        "gold_leggings.png", "gold_boots.png", "gold_sword.png", "gold_pickaxe.png", "gold_axe.png", "gold_shovel.png", "gold_hoe.png", 
        "beef_raw.png", "beef_cooked.png", "chicken_raw.png", "chicken_cooked.png", "porkchop_raw.png", "porkchop_cooked.png", "mutton_raw.png", 
        "mutton_cooked.png", "rabbit_raw.png", "rabbit_cooked.png", "fish_cod_raw.png", "fish_cod_cooked.png", "fish_salmon_raw.png", 
        "fish_salmon_cooked.png", "fish_pufferfish_raw.png", "fish_clownfish_raw.png", "melon.png", "melon_speckled.png", "apple_golden.png", 
        "carrot_golden.png", "minecart_normal.png", "door_*.png", "dye_powder_*.png", "record_*.png", "seeds_*.png", "potion_bottle_*.png", 
        "redstone_dust.png", "reeds.png", "slimeball.png", "netherbrick.png", "sign.png", "bucket_empty.png", 
        "bucket_water.png", "bucket_lava.png", "bucket_milk.png", "book_normal.png", "book_enchanted.png", "book_writable.png", "book_written.png", 
        "map_empty.png", "map_filled.png", "totem.png"
    ]
    for li in legacy_items:
        purge_glob(f"{items_dir}/{li}")
        
    purge_glob(f"{blocks_dir}/**/pumpkin_face_off.png")
    purge_glob(f"{blocks_dir}/**/pumpkin_face_on.png")

else:
    # FORMAT 1-3 / 1.12 AND BELOW - DELETE MODERN FILES
    modern_blocks = [
        "bricks.png", "potatoes_stage[0-9].png", "carrots_stage[0-9].png", "nether_wart_stage[0-9].png", "farmland.png", 
        "farmland_moist.png", "allium.png", "blue_orchid.png", "dandelion.png", "azure_bluet.png", "oxeye_daisy.png", "poppy.png", "*_tulip.png", 
        "rail.png", "powered_rail.png", "powered_rail_on.png", "detector_rail.png", "detector_rail_on.png", "activator_rail.png", "activator_rail_on.png", 
        "sandstone.png", "chiseled_sandstone.png", "cut_sandstone.png", "red_sandstone.png", "chiseled_red_sandstone.png", "cut_red_sandstone.png",
        "*_wool.png", "melon_stem.png", "attached_melon_stem.png", "pumpkin_stem.png", "attached_pumpkin_stem.png", "red_mushroom_block.png", 
        "brown_mushroom_block.png", "red_mushroom.png", "brown_mushroom.png", "mushroom_stem.png", "nether_bricks.png", "oak_door_*.png", 
        "iron_door_*.png", "spruce_door_*.png", "birch_door_*.png", "jungle_door_*.png", "acacia_door_*.png", "dark_oak_door_*.png", 
        "*_stained_glass.png", "*_stained_glass_pane_top.png", "comparator.png", "furnace_front.png", "grass_block_*.png", "terracotta.png", 
        "*_terracotta.png", "dark_prismarine.png", "prismarine.png", "oak_leaves.png", "spruce_leaves.png", "birch_leaves.png", "jungle_leaves.png", 
        "acacia_leaves.png", "dark_oak_leaves.png", "slime_block.png", "redstone_lamp.png", "piston_top.png", "anvil.png", "anvil_top.png", 
        "chipped_anvil_top.png", "damaged_anvil_top.png", "anvil_top_damaged.png", "cobweb.png", "wheat_stage[0-7].png", "smooth_stone_slab_*.png", 
        "stone_bricks.png", "mossy_stone_bricks.png", "cracked_stone_bricks.png", "chiseled_stone_bricks.png", "mossy_cobblestone.png", "*_sapling.png", 
        "redstone_torch.png", "andesite.png", "diorite.png", "granite.png", "polished_andesite.png", "polished_diorite.png", "polished_granite.png", 
        "oak_log*.png", "spruce_log*.png", "birch_log*.png", "jungle_log*.png", "acacia_log*.png", "dark_oak_log*.png", "*_planks.png", "tall_grass*.png", 
        "large_fern_*.png", "lilac_*.png", "peony_*.png", "rose_bush_*.png", "sunflower_*.png", "tripwire.png", "tripwire_hook.png", "dead_bush.png", 
        "oak_trapdoor.png", "torch.png", "itemframe_background.png", "sugar_cane.png", "wet_sponge.png", "end_portal_frame_*.png", 
        "dropper_front.png", "dispenser_front.png", "note_block.png", "packed_ice.png", "nether_quartz_ore.png",
        "quartz_pillar_side.png", "quartz_pillar.png", "quartz_pillar_top.png", "cocoa_stage0.png", "cocoa_stage1.png", "cocoa_stage2.png"
    ]
    for mb in modern_blocks:
        purge_glob(f"{blocks_dir}/{mb}")

    modern_items = [
        "map.png", "filled_map.png", "filled_map_markings.png", "poisonous_potato.png", "baked_potato.png", "fishing_rod.png", "fire_charge.png", 
        "firework_rocket.png", "armor_stand.png", "wooden_sword.png", "wooden_pickaxe.png", "wooden_axe.png", "wooden_shovel.png", "wooden_hoe.png", 
        "golden_helmet.png", "golden_chestplate.png", "golden_leggings.png", "golden_boots.png", "golden_sword.png", "golden_pickaxe.png", 
        "golden_axe.png", "golden_shovel.png", "golden_hoe.png", "beef.png", "cooked_beef.png", "chicken.png", "cooked_chicken.png", "porkchop.png", 
        "cooked_porkchop.png", "mutton.png", "cooked_mutton.png", "rabbit.png", "cooked_rabbit.png", "cod.png", "cooked_cod.png", "salmon.png", 
        "cooked_salmon.png", "pufferfish.png", "tropical_fish.png", "melon_slice.png", "glistering_melon_slice.png", "golden_apple.png", "golden_carrot.png", 
        "sugar_cane.png", "slime_ball.png", "nether_brick.png", "totem_of_undying.png", "book.png", "enchanted_book.png", "writable_book.png", 
        "written_book.png", "potion.png", "glass_bottle.png", "bucket.png", "water_bucket.png", "lava_bucket.png", "milk_bucket.png", "redstone.png", 
        "bone_meal.png", "cocoa_beans.png", "lapis_lazuli.png", "ink_sac.png", "wheat_seeds.png", "melon_seeds.png", "pumpkin_seeds.png", "music_disc_*.png", 
        "minecart.png", "chest_minecart.png", "furnace_minecart.png", "tnt_minecart.png", "hopper_minecart.png", "command_block_minecart.png", "oak_door.png", 
        "spruce_door.png", "birch_door.png", "jungle_door.png", "acacia_door.png", "dark_oak_door.png", "iron_door.png", "oak_sign.png", 
        "spruce_sign.png", "birch_sign.png", "jungle_sign.png", "acacia_sign.png", "dark_oak_sign.png", "cod_bucket.png", "salmon_bucket.png", 
        "pufferfish_bucket.png", "tropical_fish_bucket.png"
    ]
    for mi in modern_items:
        purge_glob(f"{items_dir}/{mi}")

    purge_glob(f"{blocks_dir}/carved_pumpkin.png")
    purge_glob(f"{blocks_dir}/jack_o_lantern.png")

if fmt >= 5:
    purge_glob(f"{blocks_dir}/*trapdoor*.png")
elif fmt < 4:
    for t_file in glob.glob(os.path.join(base_dir, blocks_dir, "*trapdoor*.png")):
        basename = os.path.basename(t_file)
        if basename != "trapdoor.png":
            purge_glob(f"{blocks_dir}/{basename}")

# Lectern: Prune under 1.14 (fmt < 4) and above 1.18 (fmt > 8)
if fmt < 4 or fmt > 8:
    purge_glob(f"{blocks_dir}/lectern*.png")

# Cocoa Stages: Pruned ONLY above 1.19 (fmt > 9)
if fmt > 9:
    purge_glob(f"{blocks_dir}/cocoa_stage*.png")

# Pistons: Pruned above 1.19 (fmt > 9)
if fmt > 9:
    purge_glob(f"{blocks_dir}/piston*.png")

if fmt >= 5:
    # 1.15+ Bucket Retextures
    purge_glob(f"{items_dir}/*_bucket.png") 
    purge_glob(f"{items_dir}/beetroot_seeds.png")
    purge_glob(f"{items_dir}/seeds_beetroot.png")

# The Giant Above 1.14 Block (fmt >= 5)
if fmt >= 5:
    # Planks and Logs (apart from spruce planks handled separately)
    wood_types = ["oak", "birch", "jungle", "acacia", "dark_oak", "mangrove", "cherry", "crimson", "warped", "bamboo", "bamboo_mosaic"]
    for w in wood_types:
        purge_glob(f"{blocks_dir}/{w}_planks.png")
        purge_glob(f"{blocks_dir}/planks_{w}.png")
        purge_glob(f"{blocks_dir}/{w}_log.png")
        purge_glob(f"{blocks_dir}/log_{w}.png")
        purge_glob(f"{blocks_dir}/{w}_log_top.png")
        purge_glob(f"{blocks_dir}/log_{w}_top.png")
        purge_glob(f"{blocks_dir}/{w}_stem.png")
        purge_glob(f"{blocks_dir}/{w}_stem_top.png")
    
    # Spruce logs specifically
    purge_glob(f"{blocks_dir}/spruce_log.png")
    purge_glob(f"{blocks_dir}/log_spruce.png")
    purge_glob(f"{blocks_dir}/spruce_log_top.png")
    purge_glob(f"{blocks_dir}/log_spruce_top.png")
    purge_glob(f"{blocks_dir}/spruce_stem.png")
    purge_glob(f"{blocks_dir}/spruce_stem_top.png")
    if fmt >= 8: # Spruce planks on 1.18+
        purge_glob(f"{blocks_dir}/spruce_planks.png")
        purge_glob(f"{blocks_dir}/planks_spruce.png")

    # Sponges
    purge_glob(f"{blocks_dir}/sponge.png")
    purge_glob(f"{blocks_dir}/wet_sponge.png")
    purge_glob(f"{blocks_dir}/sponge_wet.png")

    # Polished Stones
    purge_glob(f"{blocks_dir}/polished_*.png")

    # Bricks (apart from nether bricks, which remain via normal logic)
    purge_glob(f"{blocks_dir}/bricks.png")
    purge_glob(f"{blocks_dir}/brick.png")

    # Droppers and Dispensers
    purge_glob(f"{blocks_dir}/dropper_*.png")
    purge_glob(f"{blocks_dir}/dispenser_*.png")

    # Stone (All Types)
    purge_glob(f"{blocks_dir}/stone.png")
    purge_glob(f"{blocks_dir}/andesite.png")
    purge_glob(f"{blocks_dir}/diorite.png")
    purge_glob(f"{blocks_dir}/granite.png")
    purge_glob(f"{blocks_dir}/stone_andesite.png")
    purge_glob(f"{blocks_dir}/stone_diorite.png")
    purge_glob(f"{blocks_dir}/stone_granite.png")

    # Stripped Wood (apart from dark oak and spruce top)
    all_stripped = wood_types + ["spruce"]
    for w in all_stripped:
        if w != "dark_oak":
            purge_glob(f"{blocks_dir}/stripped_{w}_log.png")
            purge_glob(f"{blocks_dir}/stripped_{w}_stem.png")
        if w != "spruce":
            purge_glob(f"{blocks_dir}/stripped_{w}_log_top.png")
            purge_glob(f"{blocks_dir}/stripped_{w}_stem_top.png")
    purge_glob(f"{blocks_dir}/stripped_dark_oak_log_top.png") # Ensure dark oak top is pruned

    # Waterlily
    purge_glob(f"{blocks_dir}/lily_pad.png")
    purge_glob(f"{blocks_dir}/waterlily.png")

    # Webs
    purge_glob(f"{blocks_dir}/cobweb.png")
    purge_glob(f"{blocks_dir}/web.png")

    # Beds
    purge_glob(f"{blocks_dir}/*_bed_*.png")
    purge_glob(f"{blocks_dir}/bed_*.png")

    # Flowers (apart from dandelion)
    # Target exact names to prevent mistakenly clipping dandelion.png
    flower_patterns = ["poppy", "blue_orchid", "allium", "azure_bluet", "oxeye_daisy", "cornflower", "lily_of_the_valley", "wither_rose", "sunflower", "lilac", "peony", "rose_bush", "tulip", "flower_"]
    for fp in flower_patterns:
        if fp == "flower_":
            # Prune flower_*.png except flower_dandelion.png and flower_pot.png (it's not a flower)
            for f_file in glob.glob(os.path.join(base_dir, blocks_dir, "flower_*.png")):
                if "dandelion" not in f_file and "pot" not in f_file:
                    purge_glob(f"{blocks_dir}/{os.path.basename(f_file)}")
        elif fp == "tulip":
            purge_glob(f"{blocks_dir}/*_tulip.png")
        else:
            purge_glob(f"{blocks_dir}/{fp}*.png")

    # Normal Torches
    purge_glob(f"{blocks_dir}/torch.png")
    purge_glob(f"{blocks_dir}/torch_on.png")

    # Slabs
    purge_glob(f"{blocks_dir}/*_slab*.png")
    purge_glob(f"{blocks_dir}/stone_slab_*.png")

    # Slime Blocks
    purge_glob(f"{blocks_dir}/slime_block.png")
    purge_glob(f"{blocks_dir}/slime.png")

    # Leaves
    purge_glob(f"{blocks_dir}/*_leaves*.png")
    purge_glob(f"{blocks_dir}/leaves_*.png")

    # Spawners
    purge_glob(f"{blocks_dir}/spawner.png")
    purge_glob(f"{blocks_dir}/mob_spawner.png")

    # Sandstones and Sand Variants
    purge_glob(f"{blocks_dir}/sand.png")
    purge_glob(f"{blocks_dir}/red_sand.png")
    purge_glob(f"{blocks_dir}/*sandstone*.png")

    # Gravel
    purge_glob(f"{blocks_dir}/gravel.png")

    # Anvil Textures
    purge_glob(f"{blocks_dir}/anvil*.png")

    # Rails
    purge_glob(f"{blocks_dir}/*rail*.png")

    # Bone Blocks
    purge_glob(f"{blocks_dir}/bone_block*.png")

    # Bookshelves
    purge_glob(f"{blocks_dir}/bookshelf.png")

    # Mushroom Blocks and Mushrooms
    purge_glob(f"{blocks_dir}/*_mushroom*.png")
    purge_glob(f"{blocks_dir}/mushroom_*.png")

    # Cactuses
    purge_glob(f"{blocks_dir}/cactus*.png")

    # Cakes
    purge_glob(f"{blocks_dir}/cake*.png")

    # Cauldrons
    purge_glob(f"{blocks_dir}/cauldron*.png")

    # Clay
    purge_glob(f"{blocks_dir}/clay.png")

    # Chorus Flowers and Plant
    purge_glob(f"{blocks_dir}/chorus_*.png")

    # Crafting Tables
    purge_glob(f"{blocks_dir}/crafting_table*.png")

    # Daylight Detectors
    purge_glob(f"{blocks_dir}/daylight_detector*.png")

    # Dirt and Grass Types like Podzol and Mycelium
    dirt_basenames = [
        "dirt.png", "coarse_dirt.png", "rooted_dirt.png", 
        "dirt_path_side.png", "dirt_path_top.png", 
        "grass_path_side.png", "grass_path_top.png", 
        "podzol_side.png", "podzol_top.png",
        "mycelium_top.png", "grass_block_top.png", "grass_block_side.png",
        "grass_top.png", "grass_side.png"
    ]
    for db in dirt_basenames:
        purge_glob(f"{blocks_dir}/{db}")
        
    # Exceptions for Snowy Grass and Mycelium Side
    if fmt < 8: # Keep snowy grass above 1.17 (prune under 1.18)
        purge_glob(f"{blocks_dir}/grass_block_snow.png")
        purge_glob(f"{blocks_dir}/grass_side_snowed.png")
    if fmt <= 9: # Keep mycelium side above 1.19 (prune under 1.20)
        purge_glob(f"{blocks_dir}/mycelium_side.png")

    # Purpur Blocks and Pillars
    purge_glob(f"{blocks_dir}/purpur*.png")

    # Quartz Blocks
    purge_glob(f"{blocks_dir}/quartz*.png")
    purge_glob(f"{blocks_dir}/chiseled_quartz*.png")

    # Redstone Blocks
    purge_glob(f"{blocks_dir}/redstone_block.png")

    # End Frames (apart from eyes)
    purge_glob(f"{blocks_dir}/end_portal_frame_top.png")
    purge_glob(f"{blocks_dir}/end_portal_frame_side.png")
    purge_glob(f"{blocks_dir}/endframe_top.png")
    purge_glob(f"{blocks_dir}/endframe_side.png")

    # Resource Blocks
    for b in ["diamond", "emerald", "coal", "gold", "iron", "lapis", "lapis_lazuli"]: 
        purge_glob(f"{blocks_dir}/{b}_block.png")

    # Cobblestone and its variants
    purge_glob(f"{blocks_dir}/cobblestone*.png")
    purge_glob(f"{blocks_dir}/mossy_cobblestone.png")

    # Observer (apart from its back texture)
    purge_glob(f"{blocks_dir}/observer_top.png")
    purge_glob(f"{blocks_dir}/observer_side.png")
    purge_glob(f"{blocks_dir}/observer_front.png")

    # Sugarcane
    purge_glob(f"{blocks_dir}/sugar_cane.png")
    purge_glob(f"{blocks_dir}/reeds.png")

    # Crops and their Stages
    crop_types = ["wheat", "carrots", "potatoes", "nether_wart", "beetroots", "carrot", "potato"]
    for c in crop_types:
        purge_glob(f"{blocks_dir}/{c}_stage*.png")


# Melons, Vines, and Tall Grass: Pruned above 1.10 (fmt >= 3)
if fmt >= 3:
    purge_glob(f"{blocks_dir}/melon*.png")
    purge_glob(f"{blocks_dir}/vine*.png")
    purge_glob(f"{blocks_dir}/tall_grass*.png")
    purge_glob(f"{blocks_dir}/tallgrass.png")

if fmt < 3:
    for color in bed_colors:
        purge_glob(f"{blocks_dir}/{color}_bed_*.png")

if fmt <= 2:
    purge_glob(f"{blocks_dir}/red_nether_bricks.png")

if fmt == 1:
    purge_glob(f"{blocks_dir}/magma.png")
    purge_glob(f"{blocks_dir}/nether_wart_block.png")
    purge_glob(f"{blocks_dir}/chorus_*.png")
    purge_glob(f"{blocks_dir}/end_bricks.png")
    purge_glob(f"{items_dir}/*_boat.png")
    purge_glob(f"{items_dir}/spectral_arrow*")
    purge_glob(f"{items_dir}/dragon_breath*")
    purge_glob(f"{items_dir}/splash_potion*")
    purge_glob(f"{items_dir}/lingering_potion*")
    purge_glob(f"{items_dir}/elytra*")
    purge_glob(f"{items_dir}/chorus_fruit*")
    purge_glob(f"{items_dir}/popped_chorus_fruit*")
    purge_glob(f"{items_dir}/beetroot*")
    purge_glob(f"{items_dir}/end_crystal*")
    purge_glob(f"{items_dir}/empty_armor_slot_shield*")
    for color in bed_colors:
        purge_glob(f"{blocks_dir}/{color}_bed_*")

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